from django.contrib import admin

# Register your models here.
from .models import StoreVote
from .models import CandidateVotes

class StoreVoteAdmin(admin.ModelAdmin):
	list_display = ['specialkey','timestamp']
	search_fields = ['specialkey']
	class Meta:
		model = StoreVote


admin.site.register(StoreVote,StoreVoteAdmin)



class CandidateVotesAdmin(admin.ModelAdmin):
	list_display = ['candidate','votes']
	class Meta:
		model = CandidateVotes



admin.site.register(CandidateVotes,CandidateVotesAdmin)
