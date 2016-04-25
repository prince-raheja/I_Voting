from __future__ import unicode_literals

from django.db import models
from accounts.models import Student

# Create your models here.

class CommonBlog(models.Model):
	student = models.ForeignKey(Student,on_delete=models.CASCADE)
	content = models.TextField(blank=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return self.content

	def __unicode__(self):
		return self.content

	class Meta:
		ordering = ['-timestamp','student']
