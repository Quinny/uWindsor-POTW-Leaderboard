from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^solvers/?$', views.solvers),
    url(r'^solution_count/?$', views.problem_solution_count),
    url(r'^solution_languages/?$', views.solution_languages),
]
