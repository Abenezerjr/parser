from io import BytesIO
from django.shortcuts import render
from docx import Document
from django.core.exceptions import ValidationError
from pdfminer.high_level import extract_text

def extract_text_from_docx_file(doc):
    try:
        document = Document(doc)
        full_text = []
        for paragraph in document.paragraphs:
            full_text.append(paragraph.text)
        return '\n'.join(full_text)
    except Exception as e:
        raise ValidationError("The uploaded file is not a valid DOCX document.")

# def extract_text_from_pdf_file(pdf):
#     try:
#         text = extract_text(pdf)
#         return text
#     except Exception as e:
#         raise ValidationError("The uploaded file is not a valid PDF document.")

def extract_text_from_pdf_file(pdf):
    try:
        # Use BytesIO to read the file in binary mode
        pdf_data = pdf.read()
        pdf_io = BytesIO(pdf_data)
        # Extract text using pdfminer
        text = extract_text(pdf_io)
        return text
    except Exception as e:
        raise ValidationError("The uploaded file is not a valid PDF document.")

def home(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file:
            return render(request, 'document/index.html', {'error': 'No file uploaded'})

        file_ext = file.name.split('.')[-1].lower()

        if file_ext == 'docx':
            try:
                text = extract_text_from_docx_file(file)
            except ValidationError as ve:
                return render(request, 'document/index.html', {'error': str(ve)})
        elif file_ext == 'pdf':
            try:
                text = extract_text_from_pdf_file(file)
            except ValidationError as ve:
                return render(request, 'document/index.html', {'error': str(ve)})
        else:
            return render(request, 'document/index.html', {'error': 'Unsupported file format. Please upload a DOCX or PDF file.'})

        context = {
            'doc_text': text
        }

        return render(request, 'document/index.html', context)

    return render(request, 'document/index.html')
