from django import template
from django.template.defaulttags import register
from candidatesbulletin.models import StudentsComments
from accounts.models import Student
from accounts.models import Candidate 
from candidatesbulletin.models import CandidatePosts

register = template.Library()


@register.filter(name='getcomments')
def getcomments(comments,post):
	return comments[post]

register.filter('getcomments',getcomments)


@register.filter
def getmorevalue(more,index):
	return more[index]

# regsiter.filter('getmorevalue',getmorevalue)
