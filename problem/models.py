from django.db import models
from solution.models import Solution

class Problem(models.Model):
    year = models.IntegerField()
    week = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return str(self.year) + " Week " + str(self.week)

    def solutions(self):
        return Solution.objects.filter(year=self.year, week=self.week)
