from django.shortcuts import render , HttpResponse
from pdfminer.high_level import extract_text
from django.conf import settings
import os
from docx import Document
# Create your views here.


def extract_text_from_docx_file(docx_path):
    doc = Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)






def home(request):
  file = os.path.join(settings.BASE_DIR, 'static', 'document', 'resume-sample.pdf')
  text = extract_text(file)
  doc= os.path.join(settings.BASE_DIR,'static','document','resume2024.docx')
  doc_text = extract_text_from_docx_file(doc)
  context={
    'text':text,
    'doc_text':doc_text
  }


  return render(request,'document/index.html',context)




