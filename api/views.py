from django.http import JsonResponse
from student.models import Student

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
