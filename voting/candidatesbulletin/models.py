from __future__ import unicode_literals
from django.db import models

# Create your models here.

from accounts.models import Student
from accounts.models import Candidate


class CandidatePosts(models.Model):
	candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE)
	content = models.TextField(blank=False,default='')
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return self.content

	def __unicode__(self):
		return self.content

	class Meta:
		ordering = ['candidate','-timestamp']




class StudentsComments(models.Model):
	student = models.ForeignKey(Student,on_delete=models.CASCADE)
	post = models.ForeignKey(CandidatePosts,on_delete=models.CASCADE)
	comment = models.TextField(blank=False,default='')
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return self.comment

	def __unicode__(self):
		return self.comment

	class Meta:
		ordering = ['student','-timestamp']




class StudentLikes(models.Model):
	student = models.ForeignKey(Student,on_delete=models.CASCADE)
	post = models.ForeignKey(CandidatePosts,on_delete=models.CASCADE)
	liked = models.BooleanField(default=False)
	updated = models.DateTimeField(auto_now=True,auto_now_add=False)

	def __str__(self):
		return self.liked

	def __unicode__(self):
		return self.liked

	class Meta:
		ordering = ['student','-updated']
