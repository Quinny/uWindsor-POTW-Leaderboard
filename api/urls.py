from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^solvers/?$', views.solvers),
    url(r'^solution_count/?$', views.problem_solution_count)
)
