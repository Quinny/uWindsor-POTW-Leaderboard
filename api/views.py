from django.http import JsonResponse
from student.models import Student
from problem.models import Problem
from solution.models import Solution

def cors_json(resp):
    r = JsonResponse(resp)
    r['Access-Control-Allow-Origin'] = '*'
    r['Access-Control-Allow-Methods'] = "GET"
    r['Access-Control-Allow-Headers'] = 'X-Requested-With,content-type'
    return r

def solvers(request):
    # TODO - change this when someone else runs the show.
    students = Student.objects.exclude(student_id="perfettq")

    def latest_or_zero(student):
        try:
            return student.solution_set.latest("id").id
        except:
            return 0

    def clean(student):
        return {
            "student_id": student.student_id,
            "solved"    : student.solution_count,
            "latest_solution_id": latest_or_zero(student)
        }

    return cors_json({'data' : map(clean, students)})

def problem_solution_count(request):
    problems = Problem.objects.filter(published=True).order_by("week")

    def clean(problem):
        return {
            "week": problem.week,
            "year": problem.year,
            "solutions": Solution.objects.filter(week=problem.week, accepted=True).count()
        }

    return cors_json({'data': map(clean, problems)})
