from django.shortcuts import render
from student.models import Student
from solution.models import Solution
from problem.models import Problem
from datetime import date
import errorpage

def problem_stats(request, year, week, error=None, success=None):
    try:
        solutions = Solution.objects.filter(year=year, week=week, accepted=True)
        problem = Problem.objects.get(year=year, week=week)
        return render(request, "problem/index.html",
            {"solutions" : solutions,
             "problem"   : problem,
             "percent" :
             round(100 * (solutions.count() / float(Student.objects.count())), 2),
             "error"      : error,
             "success"    : success
            })
    except:
        return errorpage.views.index(request)

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
