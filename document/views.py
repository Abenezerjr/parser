from django.shortcuts import render , HttpResponse
from pdfminer.high_level import extract_text
from django.conf import settings
import os
# Create your views here.





def home(request):
  file = os.path.join(settings.BASE_DIR, 'static', 'document', 'resume-sample.pdf')
  text = extract_text(file)

  context={
    'text':text
  }
  return render(request,'document/index.html',context)