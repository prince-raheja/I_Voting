import re
import random
from fractions import gcd
import gmpy
import math
import time
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
from accounts.models import Student
from accounts.models import Candidate
from castvote.models import StoreVote


def home(request):
	return render(request,'administrator/home.html')


def get_votes_view(request):
	return render(request,'administrator/untitled.html')

def get_votes(request):
	context = {}
	errors = []
	if request.user.is_authenticated() and request.user.username == 'prince':
		if request.method == 'POST':
			uniquekey = request.POST.get('uniquekey','')
			year = request.POST.get('year','')
			uniquekey = uniquekey.strip().rstrip()
			if uniquekey == '':
				context["error_uniquekey"] = "* Please enter unique key"
				errors.append(None)

			if year == '':
				context["error_year"] = "* Please Enter Year"
			else:
				if year not in ['I','II','III','IV']:
					context['error_year'] = "* Please Select Correct Year"


			for error in errors:
				if error is None:
					return render(request,'administrator/untitled.html',context)

			else:
				try :
					vote = StoreVote.objects.get(specialkey=uniquekey)

					if vote.year != year:
						return HttpResponse("Invalid Year Entered")

					decrypted_keys = get_decrypted_keys()

					general_sec = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='General Secretary').order_by('student__username')
					cultural_sec = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Cultural Secretary').order_by('student__username')
					technical_sec = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Technical Secretary').order_by('student__username')
					sports_sec = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Sports Secretary').order_by('student__username')
					environmental_sec = Candidate.objects.filter(student__year=year,student__iscandidate=True, postname='Environmental Secretary').order_by('student__username')
					mess_sec = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Mess Secretary').order_by('student__username')
					maintenance_sec = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Maintenance Secretary').order_by('student__username')
					literary_sec = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Literary Secretary').order_by('student__username') 

					context['general'] = general_sec[decrypted_keys[vote.general]-1]
					context['cultural'] = cultural_sec[decrypted_keys[vote.cultural]-1]
					context['technical'] = technical_sec[decrypted_keys[vote.technical]-1]
					context['sports'] = sports_sec[decrypted_keys[vote.sports]-1]
					context['environmental'] = environmental_sec[decrypted_keys[vote.environmental]-1] 
					context['mess'] = mess_sec[decrypted_keys[vote.mess]-1]
					context['maintenance'] = maintenance_sec[decrypted_keys[vote.maintenance]-1]
					context['literary'] = literary_sec[decrypted_keys[vote.literary]-1]
					context['uniquekey'] = uniquekey

					return render(request,'administrator/result.html',context)
				except StoreVote.DoesNotExist:
					context["error_uniquekey"] = "* This key does not exist in the database"
					return render(request,'administrator/untitled.html',context)

				except Candidate.DoesNotExist:
					context['error_candidate'] = "* There is some error"

	return HttpResponse('<h3>Something bad Happended.<br></h3><br><br><a href\
				="/administrator/">Go to home</a>')


def get_encrypted_keys(p=587,q=887,max_value=10):
	n, z,e,d = generate_numbers(p,q)
	# cipher = (msg**e)%n

	en_keys = []
	
	i=0
	while i <= max_value:
		cipher = (i**e)%n
		en_keys.append(cipher)
		i = i+1

	# print "\n\n"
	# print en_keys
	# print "\n\n"
	return en_keys



def get_decrypted_keys(p=587,q=887,max_value=15):
	n,z,e,d = generate_numbers(p,q)
	# msg = (cipher**d)%n

	dec_keys = {}
	i = 0

	while i<=max_value:
		cipher = (i**e)%n
		dec_keys[cipher] = i
		i = i+1

	# print "\n\n"
	# print dec_keys
	# print "\n\n"

	return dec_keys

def generate_numbers(p=587,q=887):
	n = p*q
	z = (p-1)*(q-1)
	i = 28
	e = -2
	while i < z :
		result = calculate_gcd(i,z)
		if result == 1:
			e = i
			break
		i = i+1

	d = gmpy.invert(e,z)

	# print n, z,e,d
	return n,z,e,d


def calculate_gcd(a,b):
	return gcd(a,b)