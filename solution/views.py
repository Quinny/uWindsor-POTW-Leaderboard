from django.shortcuts import render
from student.models import Student
from django.core.mail import send_mail
from models import Solution
from problem.models import Problem
from helpers import get_or_none
from django.views.decorators.http import require_http_methods
import student
import problem.views
import errorpage

@require_http_methods(["POST"])
def add(request):
    if "source" not in request.FILES:
         return problem.views.problem_stats(request, request.POST['year'], request.POST['week'],
                "Please attach your source code")

    if "remember" in request.POST:
        request.session["submitcode"] = request.POST['submitcode']

    elif ("remember" not in request.POST) and ("submitcode" in request.session):
        del request.session["submitcode"]

    s = get_or_none(Student, submit_code=request.POST['submitcode'])
    if s is None:
        return problem.views.problem_stats(request, request.POST['year'],
                request.POST['week'], "Invalid submission code")

    extra = ""
    previous_solution = get_or_none(Solution, student=s, year=request.POST['year'],
            week=request.POST['week'])
    if previous_solution is not None and previous_solution.accepted:
        return problem.views.problem_stats(request, request.POST['year'],
                request.POST['week'], "You already have an accepted solution to this problem.")

    if previous_solution is not None and not previous_solution.accepted:
        previous_solution.delete()
        extra = "<br />Your previous submission for this problem has been deleted"

    s.solution_set.create(year=request.POST['year'], week=request.POST['week'],
            source=request.FILES['source'], public = 'public' in request.POST)

    send_mail('uWindsor POTW - ' + str(s) + ' Submission Added',
            'A submission has been added for the problem of the week!  Go check it!',
            'noreply@potw.quinnftw.com',
            # maybe dont hardcore this?
            ['perfettq@uwindsor.ca'],
            fail_silently=False)

    return problem.views.problem_stats(request, request.POST['year'], request.POST['week'],
            None, "Your code has been submitted for checking" + extra)

def show(request, solution_id):
    s = get_or_none(Solution, pk=solution_id)
    if s is None:
        return errorpage.views.index(request)

    recent_year = Problem.objects.filter(published=True).latest('year').year
    recent_week = Problem.objects.filter(published=True).latest('week').week
    context = {
        "solution":    s,
        "most_recent": s.year == recent_year and s.week == recent_week,
        "public":      s.public
    }
    return render(request, "solution/index.html", context)

def all(request):
    context = {
            "problems": Problem.objects.filter(published=True).order_by("-week")
    }
    return render(request, "solution/all.html", context)
