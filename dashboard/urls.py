from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^adduser/?$', views.add_user),
    url(r'^login/?$', views.auth_login),
    url(r'^addsolution/?$', views.add_solution),
    url(r'^addcontribution/?$', views.add_contribution),
    url(r'^student/(\d+)/?$', views.edit_student),
    url(r'^logout/?$', views.logout_page),
    url(r'^addproblem/?$', views.add_problem),
    url(r'^editproblem/(\d+)/?$', views.edit_problem),
    url(r'^updateproblem/?$', views.update_problem),
    url(r'^submission/all/?$', views.all_submissions),
    url(r'^submission/(\d+)/?$', views.mark_submission),
    url(r'^submission/accept/?$', views.accept_sub),
    url(r'^submission/decline/?$', views.decline_sub),
    url(r'^students/?$', views.all_students),
    url(r'^problems/?$', views.all_problems),
    url(r'^changepassword/?$', views.change_password),
    url(r'^draw/gen/?$', views.draw_gen),
    url(r'^draw/?$', views.draw),
)
