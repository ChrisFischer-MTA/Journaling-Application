from django.urls import path
from . import views

urlpatterns = [
    path('journals/', views.journals, name='journals'),
]
