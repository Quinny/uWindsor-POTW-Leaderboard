from django.shortcuts import render
from student.models import Student
from django.db.models import Count

def index(request):
    top_users = sorted(Student.objects.all(), key=lambda s: s.solution_count, reverse=True)
    return render(request, "student/index.html",
        {"students" : top_users })

def profile(request, pk):
    s = Student.objects.get(pk=pk)
    return render(request, "student/student.html", {"student" : s})
