from django.conf.urls import patterns, include, url
import student

urlpatterns = patterns('',
    url(r'^$',             include('student.urls')),
    url(r'^solvers/?$',    student.views.solvers),
    url(r'^student/?',     include('student.urls')),
    url(r'^dashboard/?',   include('dashboard.urls')),
    url(r'^problem/?',     include('problem.urls')),
    url(r'^solution/?',    include('solution.urls')),
    url(r'^leaderboard/?$', include ('leaderboard.urls')),
    url(r'^api/?',         include('api.urls')),
    url(r'^feed/?',        include('feed.urls')),
    url(r'^.*$',           include('errorpage.urls')),
)
