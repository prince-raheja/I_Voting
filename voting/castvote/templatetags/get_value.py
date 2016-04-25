from django import template
from django.template.defaulttags import register


register = template.Library()

@register.filter
def getvalue(encrytpedkey,index):
	return encrytpedkey[index]
