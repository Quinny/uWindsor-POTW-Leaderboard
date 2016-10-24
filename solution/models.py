from django.db import models
from student.models import Student
from os import path

languages = {
    '.asm' : 'Assembly',
    '.c' : 'C',
    '.cc' : 'C++',
    '.cs' : 'C#',
    '.cpp' : 'C++',
    '.cxx' : 'C++',
    '.f03' : 'Fortran 2003',
    '.f90' : 'Fortran 90',
    '.f95' : 'Fortran 95',
    '.hs' : 'Haskell',
    '.java' : 'Java',
    '.js' : 'JavaScript',
    '.lhs' : 'Haskell',
    '.lol' : 'LOLCODE',
    '.lols' : 'LOLCODE',
    '.py' : 'Python',
    '.rb' : 'Ruby',
    '.rs' : 'Rust',
    '.pl' : 'Prolog',
}

class Solution(models.Model):
    student = models.ForeignKey(Student)
    year = models.IntegerField()
    week = models.IntegerField()
    accepted = models.BooleanField(default=False)
    public  = models.BooleanField(default=False)
    # Default set just to make django happy
    source  = models.FileField(upload_to = "source/%Y/%m/%d", default='settings.MEDIA_ROOT/helloworld.c')
    run_time = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.year) + " Week " + str(self.week)

    def programming_language(self):
        _, ext = path.splitext(self.source.name)

        return languages.get(ext, '<a href='
                             '"https://github.com/Quinny/uWindsor-POTW-Leaderboard/blob/master/solution/models.py">'
                             'Please help</a>');


# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

@receiver(pre_delete, sender=Solution)
def solution_delete(sender, instance, **kwargs):
    instance.source.delete(False)
