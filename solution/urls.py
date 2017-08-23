from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^(\d+)/?', views.show),
    url(r'^add/?$', views.add),
    url(r'^all/?$', views.all),
]
