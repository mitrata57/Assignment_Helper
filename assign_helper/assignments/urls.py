from django.urls import path
from .views import create_assignment , assignment_detail ,respond_to_assignment

urlpatterns = [
    path('create/', create_assignment, name='create_assignment'),
    path('<int:pk>/', assignment_detail, name='assignment_detail'),
    path('assignment/<int:pk>/respond/', respond_to_assignment, name='respond_to_assignment'),
]