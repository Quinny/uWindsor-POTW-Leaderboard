from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^(\d+)/?', views.show),
    url(r'^add/?$', views.add),
    url(r'^all/?$', views.all),
)
