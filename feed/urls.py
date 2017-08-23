from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^problem/?$', views.LatestProblem()),
    url(r'^solvers/?$', views.LeaderBoard()),
]
