from django.shortcuts import render
from student.models import Student
import student
from models import Solution
from problem.models import Problem
import problem.views
import errorpage

def add(request):
    if len(request.POST['uwinid']) == 0:
        return problem.views.problem_stats(request, request.POST['year'], request.POST['week'],
                "Please specify your uWindsor ID")
    if "source" not in request.FILES:
         return problem.views.problem_stats(request, request.POST['year'], request.POST['week'],
                "Please attach your source code")

    try:
        s = Student.objects.get(student_id=request.POST['uwinid'])
    except:
        s = Student.objects.create(student_id=request.POST['uwinid'])
    s.solution_set.create(year=request.POST['year'], week=request.POST['week'], source=request.FILES['source'])

    return problem.views.problem_stats(request, request.POST['year'], request.POST['week'],
            None, "Your code has been submitted for checking")

def show(request, solution_id):
    try:
        s = Solution.objects.get(pk=solution_id)
    except:
        return errorpage.views.index(request)
    recent_year = Problem.objects.latest('year').year
    recent_week = Problem.objects.latest('week').week
    return render(request, "solution/index.html",
            {"solution" : s,
             "most_recent" : s.year == recent_year and s.week == recent_week
            })

def all(request):
    return render(request, "solution/all.html", {"problems" : Problem.objects.order_by("week")})
