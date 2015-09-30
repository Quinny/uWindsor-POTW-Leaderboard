from django.http import JsonResponse
from student.models import Student

def solvers(request):
    ret = []
    students = Student.objects.all()

    for s in students:
        ret.append({'student_id': s.student_id, 'solved': s.solution_count})
    return JsonResponse({'data': ret})
