from django.contrib.syndication.views import Feed
from problem.models import Problem
from student.models import Student

class LatestProblem(Feed):
    title = "Latest Problem Of The Week"
    link = "/feed/problem"

    def items(self):
        latest = Problem.objects.filter(published=True).order_by("-week")[0]
        return [latest]


    def item_title(self, item):
        return item.nicename

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return "/problem/" + str(item.year) + "/" + str(item.week)

class LeaderBoard(Feed):
    title = "Top Problem Solvers"
    link = "/feed/solvers"

    def items(self):
        students = Student.objects.all()
        s = sorted(students, key=lambda x: x.solution_count, reverse=True)[:5]
        return ["\n".join(map(lambda x: x.student_id, s))]

    def item_title(self, item):
        return "Top Problem Solvers"

    def item_description(self, item):
        return item

    def item_link(self, item):
        return "/solvers"

