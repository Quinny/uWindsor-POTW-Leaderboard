from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', include('student.urls')),
    url(r'^student/?', include('student.urls')),
    url(r'^dashboard/?', include('dashboard.urls')),
    url(r'^problem/?', include('problem.urls')),
    url(r'^solution/?', include('solution.urls')),
)
