from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Student(models.Model):
	username = models.CharField(max_length=40,blank=False)
	firstname = models.CharField(max_length=40,blank=False)
	lastname = models.CharField(max_length=30,blank=False)
	rollno = models.CharField(max_length=10,blank=False)
	email = models.CharField(max_length=30,blank=False)
	gender = models.CharField(max_length=6,blank=False)
	program = models.CharField(max_length=6,blank=False)
	department = models.CharField(max_length=5,blank=False)
	year = models.CharField(max_length=2,blank=False)
	iscandidate = models.BooleanField(blank=False,default=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	hasvoted = models.BooleanField(blank=False,default=False)
	updated = models.DateTimeField(auto_now=True,auto_now_add=False)

	def __str__(self):
		return self.username

	def __unicode__(self):
		return self.username

	class Meta:
		ordering = ['year','firstname','-updated','-timestamp']



class Candidate(models.Model):
	student = models.ForeignKey(Student,on_delete=models.CASCADE)
	momento = models.TextField(null=True,blank=True,default='')
	postname = models.CharField(null=True,blank=True,default='',max_length=60)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True,auto_now_add=False)

	def __str__(self):
		return self.student.username

	def __unicode__(self):
		return self.student.username


		