from django.conf.urls import url


app_name = 'commonblog'

urlpatterns = [
	url('^$','commonblog.views.list',name='commonblog_list'),
	url('^(?P<postid>\d+)/delete/$', 'commonblog.views.deleteblog', name = 'commonblog_delete'),
	url('^addblog$', 'commonblog.views.addblog', name='commonblog_add'),
]