from django.urls import path
from . import views

urlpatterns = [
    path('journals/', views.journals, name='journals'),
    path('details/<int:id>/', views.journal_detail, name='journal_detail'),  
]
