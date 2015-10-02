from django.contrib.syndication.views import Feed
from problem.models import Problem
import HTMLParser

class LatestProblem(Feed):
    title = "Latest Problem Of The Week"
    link = "/feed.xml"

    def items(self):
        latest = Problem.objects.filter(published=True).order_by("-week")[0]
        return [latest]


    def item_title(self, item):
        return item.nicename

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return "/problem/" + str(item.year) + "/" + str(item.week)
