from django.db import models
from student.models import Student

class Contribution(models.Model):
    student = models.ForeignKey(Student)
    description = models.TextField()
    commit_url = models.TextField()
    affected_page = models.TextField()

