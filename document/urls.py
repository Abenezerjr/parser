from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home, name='home'),
    # path('parsedtext/',views.clead , name='cleand')

]
