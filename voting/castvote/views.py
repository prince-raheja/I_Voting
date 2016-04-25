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
from django.core.context_processors import csrf
from accounts.models import Student
from accounts.models import Candidate
from django.contrib import messages
from .models import StoreVote
from .models import CandidateVotes


@login_required
def voting(request):
	context = {}
	if request.user.is_authenticated():
		username = request.user.username
		try:
			student = Student.objects.get(username=username)
			year = student.year
			if not student.hasvoted:
				context['general_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='General Secretary').order_by('student__username')
				context['cultural_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Cultural Secretary').order_by('student__username')
				context['technical_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Technical Secretary').order_by('student__username')
				context['sports_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Sports Secretary').order_by('student__username')
				context['environmental_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True, postname='Environmental Secretary').order_by('student__username')
				context['mess_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Mess Secretary').order_by('student__username')
				context['maintenance_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Maintenance Secretary').order_by('student__username')
				context['literary_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Literary Secretary').order_by('student__username')	

				max_value = max(context['general_sec'].count(),context['cultural_sec'].count(),context['technical_sec'].count(),\
					context['sports_sec'].count(),context['environmental_sec'].count(),context['mess_sec'].count(),\
					context['maintenance_sec'].count(),context['literary_sec'].count())	+ 3			

				encryptedkey = get_encrypted_keys(p=587,q=887,max_value=max_value)
				# for keys1 in encryptedkey:
				# 	keys1 = int(keys1)

				context['encryptedkey'] = encryptedkey

				return render(request,'castvote/castvote.html',context)

			else:
				return HttpResponse("<h3>Student has already voted</h3>")
		
		except Student.DoesNotExist:
			return HttpResponse("<h3>Student Does Not Exist</h3>")





def storevote(request):
	errors = []
	context = {}
	if request.user.is_authenticated():
		username = request.user.username
		try:
			student = Student.objects.get(username=username)
			if student.hasvoted:
				return HttpResponse("<h3>Student already voted</h3>")

		except Student.DoesNotExist:
			return HttpResponse("<h3>No student with username - " ,username, " doesn't exists in database</h3>")

		if request.method == "POST":
			try:
				general 	= request.POST.get('general','')
				cultural 	= request.POST.get('cultural','')
				technical 	= request.POST.get('technical','')
				sports 		= request.POST.get('sports','')
				environmental = request.POST.get('environmental','')
				mess 		= request.POST.get('mess','')
				maintenance = request.POST.get('maintenance','')
				literary 	= request.POST.get('literary','')


				# print "\n\n"
				# print general,cultural,technical,sports
				# print "\n\n"


				encryptedkey = get_encrypted_keys(p=587,q=887,max_value=25)
				for keys1 in encryptedkey:
					keys1 = int(keys1)

				# print "\n\n"
				# print "encryptedkey in view ", encryptedkey
				# print "\n\n"

				if is_number(general):
					if int(general) not in encryptedkey:
						context['error_general'] = '*Dont Change value in the form'
						errors.append(None)
				else:
					context['error_general'] = '*Please Select Candidate for general secretary'
					errors.append(None)

				if is_number(cultural):
					if int(cultural) not in encryptedkey:
						context['error_cultural'] = '*Dont Change value in the form'
						errors.append(None)
				else:
					context['error_cultural'] = '*Please Select Candidate for cultural secretary'
					errors.append(None)


				if is_number(technical):
					if int(technical) not in encryptedkey:
						context['error_technical'] = '*Dont Change value in the form'
						errors.append(None)
				else:
					context['error_technical'] = '*Please Select Candidate for technical secretary'
					errors.append(None)

				if is_number(sports):
					if int(sports) not in encryptedkey:
						context['error_sports'] = '*Dont Change value in the form'
						errors.append(None)
				else:
					context['error_sports'] = '*Please Select Candidate for sports secretary'
					errors.append(None)


				if is_number(environmental):
					if int(environmental) not in encryptedkey:
						context['error_environmental'] = '*Dont Change value in the form'
						errors.append(None)
				else:
					context['error_environmental'] = '*Please Select Candidate for environmental secretary'
					errors.append(None)


				if is_number(mess):
					if int(mess) not in encryptedkey:
						context['error_mess'] = '*Dont Change value in the form'
						errors.append(None)
				else:
					context['error_mess'] = '*Please Select Candidate for mess secretary'
					errors.append(None)

				
				if is_number(maintenance):
					if int(maintenance) not in encryptedkey:
						context['error_maintenance'] = '*Dont Change value in the form'
						errors.append(None)
				else:
					context['error_maintenance'] = '*Please Select Candidate for maintenance secretary'
					errors.append(None)


				if is_number(literary):
					if int(literary) not in encryptedkey:
						context['error_literary'] = '*Dont Change value in the form'
						errors.append(None)
				else:
					context['error_literary'] = '*Please Select Candidate for literary secretary'
					errors.append(None)


				for error in errors:
					if error is None:
						year = student.year
		
						# context['encryptedkey'] = encryptedkey
						context['general_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='General Secretary').order_by('student__username')
						context['cultural_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Cultural Secretary').order_by('student__username')
						context['technical_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Technical Secretary').order_by('student__username')
						context['sports_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Sports Secretary').order_by('student__username')
						context['environmental_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True, postname='Environmental Secretary').order_by('student__username')
						context['mess_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Mess Secretary').order_by('student__username')
						context['maintenance_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Maintenance Secretary').order_by('student__username')
						context['literary_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Literary Secretary').order_by('student__username')

						max_value = max(context['general_sec'].count(),context['cultural_sec'].count(),context['technical_sec'].count(),\
						context['sports_sec'].count(),context['environmental_sec'].count(),context['mess_sec'].count(),\
						context['maintenance_sec'].count(),context['literary_sec'].count())	+ 3		

						encryptedkey = get_encrypted_keys(p=587,q=887,max_value=max_value)
						context['encryptedkey'] = encryptedkey

						# for keys1 in encryptedkey:
						# 	keys1 = int(keys1)

						return render(request,'castvote/castvote.html',context)


				key = unique_key()
				context['key'] = key
				year = student.year
				vote = StoreVote(specialkey=key,general=int(general),technical=int(technical),cultural=int(cultural),\
					sports=int(sports),environmental=int(environmental),mess=int(mess),maintenance=int(maintenance),literary=int(literary),year=year)
				student.hasvoted = True
				vote.save()
				student.save()

				return render(request,'castvote/votecasted.html',context) 


				
			except ValueError:
				return HttpResponse("<h3>Please Select candidate for every post</h3>") 

		else :
			return HttpResponse("<h3> Method of submission should be <strong>POST</strong></h3>")

	else :
		return HttpResponse("<h3>You are not authenticated to vote</h3>")



def countvote(request):
	candidates = Candidate.objects.all()
	if request.user.username == 'prince':
		for candidate in candidates :
			try:
				candidatevote = CandidateVotes.objects.get(candidate=candidate)
			except CandidateVotes.DoesNotExist:
				candidatevote = CandidateVotes(candidate=candidate)
				candidatevote.save()


		for year in ['I','II','III','IV']:
			general_sec = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='General Secretary').order_by('student__username')
			cultural_sec = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Cultural Secretary').order_by('student__username')
			technical_sec = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Technical Secretary').order_by('student__username')
			sports_sec = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Sports Secretary').order_by('student__username')
			environmental_sec = Candidate.objects.filter(student__year=year,student__iscandidate=True, postname='Environmental Secretary').order_by('student__username')
			mess_sec = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Mess Secretary').order_by('student__username')
			maintenance_sec = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Maintenance Secretary').order_by('student__username')
			literary_sec = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Literary Secretary').order_by('student__username')

			max_value = max(general_sec.count(),cultural_sec.count(),technical_sec.count(),\
				sports_sec.count(),environmental_sec.count(),mess_sec.count(),\
				maintenance_sec.count(),literary_sec.count()) + 3

			decryptedkey = get_decrypted_keys(p=587,q=887,max_value=max_value)

			votes = StoreVote.objects.filter(year=year)
			for vote in votes:
				if not vote.hascounted:
					voteindex = decryptedkey[vote.general] - 1
					candidatevote = CandidateVotes.objects.get(candidate=general_sec[voteindex])
					candidatevote.votes += 1
					candidatevote.save()

					voteindex = decryptedkey[vote.technical] - 1
					candidatevote = CandidateVotes.objects.get(candidate=technical_sec[voteindex])
					candidatevote.votes += 1
					candidatevote.save()

					voteindex = decryptedkey[vote.cultural] - 1
					candidatevote = CandidateVotes.objects.get(candidate=cultural_sec[voteindex])
					candidatevote.votes += 1
					candidatevote.save()

					voteindex = decryptedkey[vote.sports] - 1
					candidatevote = CandidateVotes.objects.get(candidate=sports_sec[voteindex])
					candidatevote.votes += 1
					candidatevote.save()

					voteindex = decryptedkey[vote.environmental] - 1
					candidatevote = CandidateVotes.objects.get(candidate=environmental_sec[voteindex])
					candidatevote.votes += 1
					candidatevote.save()

					voteindex = decryptedkey[vote.mess] - 1
					candidatevote = CandidateVotes.objects.get(candidate=mess_sec[voteindex])
					candidatevote.votes += 1
					candidatevote.save()

					voteindex = decryptedkey[vote.maintenance] - 1
					candidatevote = CandidateVotes.objects.get(candidate=maintenance_sec[voteindex])
					candidatevote.votes += 1
					candidatevote.save()

					voteindex = decryptedkey[vote.literary] - 1
					candidatevote = CandidateVotes.objects.get(candidate=literary_sec[voteindex])
					candidatevote.votes += 1
					candidatevote.save()
					vote.hascounted = True
					vote.save()

	
	return HttpResponseRedirect('/voting/results/')





def showresults(request):
	context = {}
	context['general_sec_I'] = CandidateVotes.objects.filter(candidate__student__year='I',candidate__postname='General Secretary').order_by('-votes')
	context['general_sec_II'] = CandidateVotes.objects.filter(candidate__student__year='II',candidate__postname='General Secretary').order_by('-votes')
	context['general_sec_III'] = CandidateVotes.objects.filter(candidate__student__year='III',candidate__postname='General Secretary').order_by('-votes')
	context['general_sec_IV'] = CandidateVotes.objects.filter(candidate__student__year='IV',candidate__postname='General Secretary').order_by('-votes')


	context['cultural_sec_I'] = CandidateVotes.objects.filter(candidate__student__year='I',candidate__postname='Cultural Secretary').order_by('-votes')
	context['cultural_sec_II'] = CandidateVotes.objects.filter(candidate__student__year='II',candidate__postname='Cultural Secretary').order_by('-votes')
	context['cultural_sec_III'] = CandidateVotes.objects.filter(candidate__student__year='III',candidate__postname='Cultural Secretary').order_by('-votes')
	context['cultural_sec_IV'] = CandidateVotes.objects.filter(candidate__student__year='IV',candidate__postname='Cultural Secretary').order_by('-votes')


	context['technical_sec_I'] = CandidateVotes.objects.filter(candidate__student__year='I',candidate__postname='Technical Secretary').order_by('-votes')
	context['technical_sec_II'] = CandidateVotes.objects.filter(candidate__student__year='II',candidate__postname='Technical Secretary').order_by('-votes')
	context['technical_sec_III'] = CandidateVotes.objects.filter(candidate__student__year='III',candidate__postname='Technical Secretary').order_by('-votes')
	context['technical_sec_IV'] = CandidateVotes.objects.filter(candidate__student__year='IV',candidate__postname='Technical Secretary').order_by('-votes')


	context['sports_sec_I'] = CandidateVotes.objects.filter(candidate__student__year='I',candidate__postname='Sports Secretary').order_by('-votes')
	context['sports_sec_II'] = CandidateVotes.objects.filter(candidate__student__year='II',candidate__postname='Sports Secretary').order_by('-votes')
	context['sports_sec_III'] = CandidateVotes.objects.filter(candidate__student__year='III',candidate__postname='Sports Secretary').order_by('-votes')
	context['sports_sec_IV'] = CandidateVotes.objects.filter(candidate__student__year='IV',candidate__postname='Sports Secretary').order_by('-votes')


	context['environmental_sec_I'] = CandidateVotes.objects.filter(candidate__student__year='I',candidate__postname='Environmental Secretary').order_by('-votes')
	context['environmental_sec_II'] = CandidateVotes.objects.filter(candidate__student__year='II',candidate__postname='Environmental Secretary').order_by('-votes')
	context['environmental_sec_III'] = CandidateVotes.objects.filter(candidate__student__year='III',candidate__postname='Environmental Secretary').order_by('-votes')
	context['environmental_sec_IV'] = CandidateVotes.objects.filter(candidate__student__year='IV',candidate__postname='Environmental Secretary').order_by('-votes')


	context['mess_sec_I'] = CandidateVotes.objects.filter(candidate__student__year='I',candidate__postname='Mess Secretary').order_by('-votes')
	context['mess_sec_II'] = CandidateVotes.objects.filter(candidate__student__year='II',candidate__postname='Mess Secretary').order_by('-votes')
	context['mess_sec_III'] = CandidateVotes.objects.filter(candidate__student__year='III',candidate__postname='Mess Secretary').order_by('-votes')
	context['mess_sec_IV'] = CandidateVotes.objects.filter(candidate__student__year='IV',candidate__postname='Mess Secretary').order_by('-votes')


	context['maintenance_sec_I'] = CandidateVotes.objects.filter(candidate__student__year='I',candidate__postname='Maintenance Secretary').order_by('-votes')
	context['maintenance_sec_II'] = CandidateVotes.objects.filter(candidate__student__year='II',candidate__postname='Maintenance Secretary').order_by('-votes')
	context['maintenance_sec_III'] = CandidateVotes.objects.filter(candidate__student__year='III',candidate__postname='Maintenance Secretary').order_by('-votes')
	context['maintenance_sec_IV'] = CandidateVotes.objects.filter(candidate__student__year='IV',candidate__postname='Maintenance Secretary').order_by('-votes')


	context['literary_sec_I'] = CandidateVotes.objects.filter(candidate__student__year='I',candidate__postname='Literary Secretary').order_by('-votes')
	context['literary_sec_II'] = CandidateVotes.objects.filter(candidate__student__year='II',candidate__postname='Literary Secretary').order_by('-votes')
	context['literary_sec_III'] = CandidateVotes.objects.filter(candidate__student__year='III',candidate__postname='Literary Secretary').order_by('-votes')
	context['literary_sec_IV'] = CandidateVotes.objects.filter(candidate__student__year='IV',candidate__postname='Literary Secretary').order_by('-votes')


	return render(request,'castvote/votingresults.html',context)



def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False



def unique_key():
	string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'
	try:
		while(True):
			key = ''.join(random.choice(string) for i in range(16))
			vote = StoreVote.objects.get(specialkey=key)

	except StoreVote.DoesNotExist:
		return str(key)



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

# def printga():
# 	print "\n\n"
# 	print "general  = ", general
# 	print "cultural = ", cultural
# 	print "technical = ", technical
# 	print "sports = ",sports
# 	print "environmental = ", environmental
# 	print "mess  = ",mess
# 	print "maintenance  = ", maintenance
# 	print "literary  = ",literary
# 	print "\n\n"

# 	# general 	= int(request.POST.get('general',''))
# 	# cultural 	= int(request.POST.get('cultural',''))
# 	# technical 	= int(request.POST.get('technical',''))
# 	# sports 		= int(request.POST.get('sports',''))
# 	# environmental = int(request.POST.get('environmental',''))
# 	# mess 		= int(request.POST.get('mess',''))
# 	# maintenance = int(request.POST.get('maintenance',''))
# 	# literary 	= int(request.POST.get('literary',''))

