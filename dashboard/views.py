from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from student.models import Student
from problem.models import Problem
from solution.models import Solution
from django.core.mail import send_mail
import random

def index(request, error = None, success = None):
    if request.user.is_authenticated():
        context = {
            "pending_submissions": Solution.objects.filter(accepted=False).count(),
             "error":              error,
             "success":            success
        }
        return render(request, "dashboard/admin.html", context)
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
def add_contribution(request):
    if request.method == "POST":
        s = Student.objects.get(pk=request.POST['pk'])
        s.contribution_set.create(description=request.POST['description'],
                commit_url=request.POST['commit-url'],
                affected_page=request.POST['affected-page'])
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
                                   description=request.POST['description'],
                                   nicename=request.POST['nicename'],
                                   published='publish' in request.POST)
        p.save()
    return redirect("/dashboard/")

@login_required
def edit_problem(request, pk):
    p = Problem.objects.get(pk=pk)
    return render(request, "dashboard/problem.html",{ "problem" : p})

@login_required
def update_problem(request):
    if request.method == "POST":
        to_update = Problem.objects.get(pk=request.POST['pk'])
        to_update.week = request.POST['week']
        to_update.year = request.POST['year']
        to_update.description = request.POST['description']
        to_update.nicename = request.POST['nicename']
        to_update.published = 'publish' in request.POST
        to_update.save()
    return redirect("/problem/" + request.POST['year'] + "/" + request.POST['week'])

@login_required
def all_submissions(request):
    return render(request, "dashboard/submissions.html", {"submissions" : Solution.objects.filter(accepted=False)})

@login_required
def all_students(request):
    return render(request, "dashboard/students.html",
            {"students" : Student.objects.all()}
        )

@login_required
def all_problems(request):
    return render(request, "dashboard/problems.html",
            {"problems" : Problem.objects.order_by("week")}
        )

@login_required
def mark_submission(request, solution_id):
    return render(request, "dashboard/submission.html", {"submission" : Solution.objects.get(pk = solution_id)})

@login_required
def accept_sub(request):
    s = Solution.objects.get(pk=request.POST['pk'])
    s.accepted = True
    s.save()
    send_mail('uWindsor POTW - Submission Accepted',
            "Your submission for " + str(s) + " has been accepted!  Good work!",
            'noreply@potw.quinnftw.com',
            [str(s.student) + "@uwindsor.ca"],
            fail_silently=False)
    return redirect('/dashboard/submission/all')

@login_required
def decline_sub(request):
    s = Solution.objects.get(pk=request.POST['pk'])
    s.delete()
    send_mail('uWindsor POTW - Submission Declined',
            "Your submission for " + str(s) + " has been declined!\n"\
            +"Reason: " + request.POST['reason'] + "\n"\
            +"Give it another shot!",
            'noreply@potw.quinnftw.com',
            [str(s.student) + "@uwindsor.ca"],
            fail_silently=False)
    return redirect('/dashboard/submission/all')

@login_required
def change_password(request):
    u = authenticate(username = request.user.username,
            password = request.POST['current-password'])
    if u is not None:
        request.user.set_password(request.POST['new-password'])
        request.user.save()
        return index(request, None, "Password changed")
    else:
        return index(request, "Wrong current password")

@login_required
def draw(request):
    years = Problem.objects.order_by("year").values_list("year", flat=True).distinct()
    weeks = Problem.objects.order_by("week").values_list("week", flat=True).distinct()
    return render(request, "dashboard/draw.html",
            {"years" : years, "weeks" : weeks})

@login_required
def draw_gen(request):
    candidates = Solution.objects.filter(year=request.POST['year'], accepted=True,
            week__range=(request.POST['start-week'], request.POST['end-week']))
    winner = random.choice(candidates).student
    return render(request, "dashboard/winner.html", {"winner" : winner})
