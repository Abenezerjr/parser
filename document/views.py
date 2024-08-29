from io import BytesIO
from django.shortcuts import render
from docx import Document
from django.core.exceptions import ValidationError
from pdfminer.high_level import extract_text
import spacy
import re
from spacy.tokens import Doc, Span
from spacy.matcher import Matcher

nlp = spacy.load('en_core_web_sm')




def preprocess_text(text):
    """
    accept text and return Clean and preprocess text data.
    """
    # Ensure text is a string
    if not isinstance(text, str):
        raise ValueError("Input text must be a string.")
    # Step 1: Lowercase
    text = text.lower()

    # Step 2: Removing punctuation and special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Step 3: Tokenization, Stop word removal, and Lemmatization
    doc = nlp(text)
    print('doc')
    print(doc)
    tokens = []
    for token in doc:
        if not token.is_stop:
            tokens.append(token.lemma_)

    # If tokens is empty after preprocessing
    if not tokens:
        raise ValueError("Text preprocessing resulted in no tokens.")

    print(tokens)

    # Returning preprocessed text as a single string
    return ' '.join(tokens)

def extract_text_from_docx_file(doc):
    try:
        document = Document(doc)
        full_text = []
        for paragraph in document.paragraphs:
            full_text.append(paragraph.text)
        return '\n'.join(full_text)
    except Exception as e:
        raise ValidationError("The uploaded file is not a valid DOCX document.")


def extract_text_from_pdf_file(pdf):
    try:
        # Use BytesIO to read the file in binary mode
        pdf_data = pdf.read()
        pdf_io = BytesIO(pdf_data)
        print('pdf file')
        print(pdf_io)
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
                new_text = preprocess_text(text)
                # print(new_text)
            except ValidationError as ve:
                return render(request, 'document/index.html', {'error': str(ve)})
        else:
            return render(request, 'document/index.html',
                          {'error': 'Unsupported file format. Please upload a DOCX or PDF file.'})

        # Preprocess the text
        cleaned_text = preprocess_text(text)

        # Extract entities
        # entities = extract_entities(cleaned_text)

        context = {
            'doc_text': text,
            'entities': cleaned_text
        }

        return render(request, 'document/index.html', context)

    return render(request, 'document/index.html')


# def clead(request):
#     return render(request,'document/home.html')
