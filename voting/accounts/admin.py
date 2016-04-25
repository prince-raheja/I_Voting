from django.contrib import admin

# Register your models here.
from accounts.models import Student
from accounts.models import Candidate

class StudentModelAdmin(admin.ModelAdmin):
	list_display = ['username','department','iscandidate','timestamp']

	class Meta:
		model = Student


admin.site.register(Student,StudentModelAdmin)



class CandidateModelAdmin(admin.ModelAdmin):
	list_display = ['__unicode__','postname','momento']

	class Meta:
		model = Candidate


admin.site.register(Candidate,CandidateModelAdmin)