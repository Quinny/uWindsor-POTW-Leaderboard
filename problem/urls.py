from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^(\d+)/(\d+)/?$', views.problem_stats),
    url(r'^all/?$',         views.show_all),
)
