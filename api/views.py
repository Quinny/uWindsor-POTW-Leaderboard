from django.http import JsonResponse
from student.models import Student

def cors_json(resp):
    r = JsonResponse(resp)
    r['Access-Control-Allow-Origin'] = '*'
    r['Access-Control-Allow-Methods'] = "GET"
    r['Access-Control-Allow-Headers'] = 'X-Requested-With,content-type'
    return r

def solvers(request):
    ret = []
    students = Student.objects.all()

    for s in students:
        ret.append({'student_id': s.student_id, 'solved': s.solution_count})
    return cors_json({'data' : ret})
    #return JsonResponse({'data': ret})
