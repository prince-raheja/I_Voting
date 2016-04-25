from django.conf.urls import url

app_name = 'castvote'

urlpatterns = [
	url(r'^$','castvote.views.voting',name='voting'),
	url(r'^done/$','castvote.views.storevote', name='storevote'),
	url(r'^count/$','castvote.views.countvote',name='countvote'),
	url(r'^results/$','castvote.views.showresults',name='showresults'),
]
