from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from student.models import Student
from problem.models import Problem
from solution.models import Solution

def index(request):
    if request.user.is_authenticated():
        return render(request, "dashboard/admin.html",
                {"students" : Student.objects.all(),
                "problems" : Problem.objects.order_by("week"),
                "pending_submissions" : Solution.objects.filter(accepted=False).count()
                })
    return render(request, "dashboard/index.html", {})

def auth_login(request):
    if request.method == "POST":
        try:
            u = authenticate(username=request.POST['username'],
                             password=request.POST['password'])
            if u is not None:
                login(request, u)
        except:
            return redirect("/dashboard/")
    return redirect("/dashboard/")

@login_required
def logout_page(request):
    logout(request)
    return redirect("/")

@login_required
def add_user(request):
    if request.method == "POST":
        s = Student.objects.create(student_id=request.POST['student_id'])
        s.save()
    return redirect("/dashboard/")

@login_required
def add_solution(request):
    if request.method == "POST":
        s = Student.objects.get(pk=request.POST['pk'])
        s.solution_set.create(year=request.POST['year'],
                              week=request.POST['week'])
        s.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def edit_student(request, pk):
    s = Student.objects.get(pk=pk)
    return render(request, "dashboard/student.html", {"student" : s})

@login_required
def add_problem(request):
    if request.method == "POST":
        p = Problem.objects.create(year=request.POST['year'],
                                   week=request.POST['week'],
                                   description=request.POST['description'])
        p.save()
    return redirect("/dashboard/")

@login_required
def edit_problem(request, pk):
    p = Problem.objects.get(pk=pk)
    return render(request, "dashboard/editproblem.html",{ "problem" : p})

@login_required
def update_problem(request):
    if request.method == "POST":
        to_update = Problem.objects.get(pk=request.POST['pk'])
        to_update.week = request.POST['week']
        to_update.year = request.POST['year']
        to_update.description = request.POST['description']
        to_update.save()
    return redirect("/problem/" + request.POST['year'] + "/" + request.POST['week'])

@login_required
def all_submissions(request):
    return render(request, "dashboard/submissions.html", {"submissions" : Solution.objects.filter(accepted=False)})

@login_required
def mark_submission(request, solution_id):
    return render(request, "dashboard/submission.html", {"submission" : Solution.objects.get(pk = solution_id)})

@login_required
def accept_sub(request):
    s = Solution.objects.get(pk=request.POST['pk'])
    s.accepted = True
    s.save()
    # EMAIL PERSON HERE TO TELL THEM?
    return redirect('/dashboard/submission/all')

@login_required
def decline_sub(request):
    s = Solution.objects.get(pk=request.POST['pk'])
    s.delete()
    # EMAIL PERSON HERE TO TELL THEM?
    return redirect('/dashboard/submission/all')
