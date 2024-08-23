from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
#path('docx/',views.extract_text_from_docx, name='docx')

]
