from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_student, name='register_student'),
    path('students/csv/', views.export_students_csv, name='export_students_csv'),
    path('students/pdf/', views.export_students_pdf, name='export_students_pdf'),
]
