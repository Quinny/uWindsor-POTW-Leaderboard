from django.shortcuts import render
from student.models import Student
from solution.models import Solution
from problem.models import Problem
from datetime import date
from helpers import filter_or_none, get_or_none, any_none
import errorpage

def problem_stats(request, year, week, error=None, success=None):
    solutions, problem =[
        filter_or_none(Solution, year=year, week=week, accepted=True),
        get_or_none(Problem, year=year, week=week, published=True)]

    if any_none(solutions, problem):
        return errorpage.views.index(request)

    context = {
        "solutions": solutions,
        "problem":   problem,
        "percent":
        round(100 * (solutions.count() / float(Student.objects.count())), 2),
        "error":     error,
        "success":   success,
    }

    if "submitcode" in request.session:
        context["submitcode"] = request.session["submitcode"]
    return render(request, "problem/index.html", context)

def show_all(request):
    context = {
        "problems": Problem.objects.filter(published=True).order_by("week"),
    }
    return render(request, "problem/all.html", context)
