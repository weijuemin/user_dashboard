from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='ud_index'),
	url(r'^login$', views.login, name='ud_login'),
	url(r'^login/process$', views.loginProcess, name='ud_login_process'),
	url(r'^register$', views.register, name='ud_register'),
	url(r'^register/process$', views.registerProcess, name='ud_register_process'),
	# for admins to add a new user
	url(r'^users/new$', views.new, name='ud_adduser'),
	url(r'^users/new/process$', views. newProcess, name='ud_add_user_process'),
	# all users can see the dashboard
	url(r'^dashboard_display$', views.showDashboard, name='ud_show_dashboard'),
	# for all users to edit their own profile
	url(r'^users/edit$', views.editUser, name='ud_edituser'),
	url(r'^users/edit/current$', views.editUserProcess, name='ud_edituser_process'),
	# show a specific user and leave message/comments(all user fn)
	url(r'^users/show/(?P<user_id>\d+)$', views.showUser, name='ud_show_user'),
	url(r'^users/admin/remove/(?P<user_id>\d+)$', views.removeUser, name='ud_removeuser'),
	# for admins to edit any normal user
	url(r'^users/admin/edit/(?P<user_id>\d+)$', views.adminEditUser, name='ud_admin_edituser'),
	url(r'^users/admin/update/(?P<user_id>\d+)$', views.adminUpdateUser, name='ud_admin_edituser'),
	url(r'^users/show/(?P<user_id>\d+)/post$',views.messageProcess, name='ud_leave_message'),
	url(r'^users/show/(?P<user_id>\d+)/(?P<msg_id>\d+)/comment$',views.commentProcess, name='ud_leave_comment'),
	url(r'^users/logout$', views.logout, name='ud_logout'),	
	# See views for details
	# url(r'^changeuserlevel$', views.privateUserlevel)
]