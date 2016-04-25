from django.contrib import admin

# Register your models here.

from candidatesbulletin.models import CandidatePosts
from candidatesbulletin.models import StudentsComments

class CandidatePostsAdmin(admin.ModelAdmin):
	list_display = ['candidate','content','timestamp']
	search_fields = ['candidate']
	class Meta:
		model = CandidatePosts


admin.site.register(CandidatePosts,CandidatePostsAdmin)


class StudentsCommentsAdmin(admin.ModelAdmin):
	list_display = ['student','comment','timestamp']
	search_fields = ['student']
	class Meta:
		model = StudentsComments


admin.site.register(StudentsComments,StudentsCommentsAdmin)
from django.contrib import admin

# Register your models here.
