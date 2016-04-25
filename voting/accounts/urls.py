from django.conf.urls import url

app_name = 'accounts'
urlpatterns = [
	url(r'^login/$','accounts.views.login',name = 'login'),
	url(r'^auth/$','accounts.views.auth_view',name='authenticate'),
	url(r'^logout/$','accounts.views.logout',name= 'logout'),
	# url(r'^loggedin/$','accounts.views.loggedin',name='loggedin'),
	# url(r'^invalid/$','accounts.views.invalid_login',name = 'invalid_login'),
	url(r'^register/$','accounts.views.register',name='register'),
	url(r'^register_result/$', 'accounts.views.register_result',name = 'register_result'),
	url(r'^myprofile/$', 'accounts.views.myprofile', name = 'myprofile'),
	url(r'^updateprofile/$', 'accounts.views.updateprofile', name = 'updateprofile'),
	url(r'changepassword/$', 'accounts.views.changepassword', name = 'changepassword'),
	url(r'^updatepassword/$', 'accounts.views.updatepassword', name = 'updatepassword'),
	url(r'^applyforcandidate/$', 'accounts.views.applyforcandidate', name = 'applyforcandidate'),
	url(r'^candidateresult/$', 'accounts.views.candidateapplicationresult', name = 'candidateapplicationresult'),
]

