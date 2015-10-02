from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^problem/?$', views.LatestProblem()),
    url(r'^solvers/?$', views.LeaderBoard()),
)
