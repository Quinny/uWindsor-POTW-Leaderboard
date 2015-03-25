from django.db import models
from student.models import Student

class Solution(models.Model):
    student = models.ForeignKey(Student)
    year = models.IntegerField()
    week = models.IntegerField()
    accepted = models.BooleanField(default=False)
    public  = models.BooleanField(default=False)
    # Default set just to make django happy
    source  = models.FileField(upload_to = "source/%Y/%m/%d", default='settings.MEDIA_ROOT/helloworld.c')

    def __str__(self):
        return str(self.year) + " Week " + str(self.week)

# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

@receiver(pre_delete, sender=Solution)
def solution_delete(sender, instance, **kwargs):
    instance.source.delete(False)
