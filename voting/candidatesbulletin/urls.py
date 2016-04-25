from django.conf.urls import url
from django.contrib import admin

app_name = 'candidatesbulletin'

urlpatterns = [
	url(r'^$', 'candidatesbulletin.views.list', name = 'list'),
	url(r'^candidate/(?P<studentid>\d+)/$', 'candidatesbulletin.views.candidateinfo', name = 'candidateinfo'),
	url(r'^post/(?P<candidatepostid>\d+)/$','candidatesbulletin.views.fullpost', name = 'fullpost'),
	url(r'^(?P<candidatepostid>\d+)/deletepost/$','candidatesbulletin.views.deletepost', name = 'deletepost'),
	url(r'^(?P<candidatepostid>\d+)/addcomment/$','candidatesbulletin.views.addcomment', name='addcomment'),
	url(r'^(?P<candidatepostid>\d+)/(?P<commentid>\d+)/delete/$','candidatesbulletin.views.deletecomment', name='deletecomment'),
	url(r'^addpost/$','candidatesbulletin.views.addpost',name='addpost'),
	# url(r'^add/$', 'candidatesbulletin.views.add', name='add')
]


# /candidatesbulletin/{{post.id}}/{{comment.id}}/delete/