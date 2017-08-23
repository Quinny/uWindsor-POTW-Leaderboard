from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^signup/?$', views.sign_up),
    url(r'^sendmail/?$', views.send_verify),
    url(r'^verify/([^/]+)/([^/]+)/?$', views.verify),
    url(r'^([^/]+)/?$', views.profile), # make sure this is last
]
