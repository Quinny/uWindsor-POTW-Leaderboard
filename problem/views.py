from django.shortcuts import render
from student.models import Student
from solution.models import Solution
from problem.models import Problem
from datetime import date

def problem_stats(request, year, week):
    solutions = Solution.objects.filter(year=year, week=week)
    return render(request, "problem/index.html",
            {"solutions" : solutions,
             "year"      : year,
             "week"      : week,
             "percent" :
             round(100 * (solutions.count() / float(Student.objects.count())), 2),
             "description": Problem.objects.get(week=week, year=year).description
            })

def show_all(request):
    return render(request, "problem/all.html",
            {"problems" : Problem.objects.order_by("week"),
             "labels"   : graph_labels(),
             "data"     : graph_data()
            })

def graph_labels():
    problems = Problem.objects.order_by("week")
    labels = map(lambda i : '"Week ' + str(i) + '"', range(1, problems.count() + 1))
    return "labels: [" + ",".join(labels) + "]"

def graph_data():
    n = Problem.objects.all().count()
    sols = []
    for i in range(1, n + 1):
        sols.append(Solution.objects.filter(year=date.today().year, week=i, accepted=True).count())
    return "data : [" + ",".join(map(str, sols)) + "]"
