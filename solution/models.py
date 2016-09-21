from django.db import models
from student.models import Student
from os import path

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

    def programming_language(self):
        _, ext = path.splitext(self.source.name)

        if ext in languages:
            return languages[ext]
        else:
            return "Unknown"
    programming_languages.languages = {     '.py' : 'Python',
                                            '.c' : 'C',
                                            '.cpp' : 'C++',
                                            '.cxx' : 'C++',
                                            '.cc' : 'C++',
                                            '.rs' : 'Rust',
                                            '.js' : 'JavaScript',
                                            '.java' : 'Java',
                                            '.asm' : 'Assembly',
                                            '.rb' : 'Ruby',
                                            '.hs' : 'Haskell',
                                            '.lhs' : 'Haskell'
                                            '.lol' : 'LOLCODE'
                                            '.lols' : 'LOLCODE'
    }

# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

@receiver(pre_delete, sender=Solution)
def solution_delete(sender, instance, **kwargs):
    instance.source.delete(False)
