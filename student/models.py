from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length = 200, default="")

    def __str__(self):
        return self.student_id

    @property
    def solution_count(self):
        return self.solution_set.filter(accepted=True).count()

