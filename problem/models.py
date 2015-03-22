from django.db import models

class Problem(models.Model):
    year = models.IntegerField()
    week = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return str(self.year) + " Week " + str(self.week)
