from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Resume
from .serializers import ResumeSerializer
import PyPDF2
import os

# Predefined keywords for screening (customize as needed)
KEYWORDS = ['python', 'django', 'javascript', 'html', 'css', 'machine learning']

@api_view(['POST'])
def upload_and_screen_resume(request):
    serializer = ResumeSerializer(data=request.data)
    if serializer.is_valid():
        resume = serializer.save()
        # Extract text from file
        file_path = resume.file.path
        text = ""
        if file_path.endswith('.pdf'):
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        elif file_path.endswith('.txt'):
            with open(file_path, 'r') as f:
                text = f.read()
        else:
            return Response({'error': 'Unsupported file type'}, status=status.HTTP_400_BAD_REQUEST)
        
        resume.extracted_text = text.lower()
        # Simple keyword matching for score
        matches = sum(1 for keyword in KEYWORDS if keyword in resume.extracted_text)
        resume.score = (matches / len(KEYWORDS)) * 100  # Percentage
        resume.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')