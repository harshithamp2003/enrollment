from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .forms import StudentForm
from .models import Student
import csv
from io import BytesIO
from reportlab.pdfgen import canvas

def register_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = StudentForm()
    return render(request, 'enrollment/register.html', {'form': form})

def export_students_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Email', 'Date of Birth'])

    for student in Student.objects.all():
        writer.writerow([student.first_name, student.last_name, student.email, student.date_of_birth])

    return response

def export_students_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="students.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    p.drawString(100, 800, "List of Students")
    y = 750
    for student in Student.objects.all():
        p.drawString(100, y, f"{student.first_name} {student.last_name} ({student.email})")
        y -= 25

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
