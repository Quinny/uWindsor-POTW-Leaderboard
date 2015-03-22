from django.shortcuts import render
from student.models import Student
import student
from models import Solution

def add(request):
    try:
        s = Student.objects.get(student_id=request.POST['uwinid'])
    except:
        s = Student.objects.create(student_id=request.POST['uwinid'])
    s.solution_set.create(year=request.POST['year'], week=request.POST['week'], source=request.FILES['source'])
    s.save()
    return student.views.index(request)

def show(request, solution_id):
    s = Solution.objects.get(pk=solution_id)
    return render(request, "solution/index.html", {"solution" : s})
