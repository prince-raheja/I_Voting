from django.conf.urls import url

app_name = 'administrator'

urlpatterns = [
	url(r'^$','administrator.views.home',name = 'home'),
	url(r'^uniquekey/$','administrator.views.get_votes_view',name='get_votes_view'),
	url(r'^result/$','administrator.views.get_votes',name='get_votes'),
	#url(r'^$')
]