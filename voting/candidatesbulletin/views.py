import re
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from accounts.models import Student
from accounts.models import Candidate 
from .models import CandidatePosts
from .models import StudentsComments


def list(request):
	i = 0
	context = {}
	if request.user.is_authenticated():
		try:
			username = request.user.username
			student = Student.objects.get(username=username)
			context['student'] = student
			if student.iscandidate :
				candidate = Candidate.objects.get(student=student)
				context['candidate'] = candidate
		except Student.DoesNotExist:
			return HttpResponse("<h3>Student DoesNotExist </h3>")
		except Candidate.DoesNotExist:
			return HttpResponse("<h3>Candidate DoesNotExist </h3>")

	posts = CandidatePosts.objects.all().order_by('-timestamp')
	context['posts'] = posts
	# print posts
	# print "\n"
	comments = []
	more = []
	for post in posts:
		postcomments = StudentsComments.objects.all().filter(post=post).order_by('timestamp')
		comments_count = postcomments.count()
		if comments_count > 4:
			start = comments_count - 4
			end = comments_count 
			postcomments = postcomments[start:end]
			more.append(True)
		else :
			more.append(False)

		comments.append(postcomments)

	context['comments'] = comments
	context['more'] = more
	# print "********************************"
	# print posts
	# print comments
	# print more 
	# print "********************************"
	return render(request,'candidatesbulletin/postslist.html',context)


# @required.tag(name='get_comments')
# def get_comments(comments,index):
# 	return comments[int(index)]


@login_required
def addpost(request):
	context = {}
	if request.user.is_authenticated():
		try:
			username = request.user.username
			student = Student.objects.get(username=username)
			context['student'] = student
			if student.iscandidate :
				candidate = Candidate.objects.get(student=student)

				if request.method == "POST" :
					content = request.POST.get('content',None)
					path = request.POST.get('path','/commonblog/')
					# print '**********************************************\n\n'
					# print "in addpost ", path 
					# print '\n\n*************************************'
					if content != '' or content != None:
						candidatepost = CandidatePosts(candidate=candidate,content=content)
						candidatepost.save()
						return HttpResponseRedirect(path)
				else :
					return HttpResponse("<h3>Method must be post for submitting data</h3>")

			else : 
				return HttpResponse("<h3>Student Must be Candidate for posting in candidatesbulletin</h3>")
		
		except Student.DoesNotExist :
			return HttpResponse("<h3>Student does not exist</h3>")

		except Candidate.DoesNotExist :
			return HttpResponse("<h3>Error 404<h3><br>Requested Candidate Doesnot Exists in the database<br>")


@login_required
def candidateinfo(request,studentid):
	context = {}
	i = 0
	try : 
		student = Student.objects.get(id=studentid)
		if student.iscandidate:
			candidate = Candidate.objects.get(student=student)
			context['candidate'] = candidate
			posts = CandidatePosts.objects.filter(candidate=candidate).order_by('-timestamp')
			context['posts'] = posts
			comments = []
			more = []

			for post in posts:
				postcomments = StudentsComments.objects.all().filter(post=post).order_by('timestamp')
				comments_count = postcomments.count()
				if comments_count > 4:
					start = comments_count - 4
					end = comments_count 
					postcomments = postcomments[start:end]
					more.append(True)
				else:
					more.append(False)

				comments.append(postcomments)

			context['comments'] = comments
			context['more'] = more

			return render(request,'candidatesbulletin/candidateblog.html',context)

		else :
			return HttpResponse("<h3>Error 404<h3><br>Requested Candidate Doesnot Exists in the database<br>")

	except Student.DoesNotExist :
		return HttpResponse("<h3>Error 404<h3><br>Requested Student Doesnot Exists in the database<br>")

	except Candidate.DoesNotExist :
			return HttpResponse("<h3>Error 404<h3><br>Requested Candidate Doesnot Exists in the database<br>")



@login_required
def fullpost(request,candidatepostid):
	try : 
		candidatepost = CandidatePosts.objects.get(id=candidatepostid)
		comments = StudentsComments.objects.filter(post=candidatepost).order_by('timestamp')

		context = {}
		context['candidatepost'] = candidatepost 
		context['comments'] = comments

		return render(request,'candidatesbulletin/postinfo.html',context)
	except :
		return HttpResponse("<h3>Error 404<h3><br>Requested Candidate Post Doesnot Exists in the database<br>")



@login_required
def deletepost(request,candidatepostid):
	link = request.GET.get('link','/candidatesbulletin/')
	if request.user.is_authenticated:
		try:
			username = request.user.username
			student = Student.objects.get(username=username)
			if student.iscandidate :
				candidate = Candidate.objects.get(student=student)
				post = CandidatePosts.objects.get(id=candidatepostid)
				post.delete()
				return HttpResponseRedirect(link)

		except Student.DoesNotExist :
			return HttpResponse("<h3>Error 404<h3><br>Requested Student Doesnot Exists in the database<br>")

		except Candidate.DoesNotExist :
			return HttpResponse("<h3>Error 404<h3><br>Requested Candidate Doesnot Exists in the database<br>")

		except CandidatePosts.DoesNotExist :
			return HttpResponse("<h3>Error 404<h3><br>Post Doesnot Exists in the database<br>")




@login_required
def addcomment(request,candidatepostid):

	if request.user.is_authenticated():
		try:
			username = request.user.username
			student = Student.objects.get(username=username)

			if request.method == "POST" :
				comment = request.POST.get('comment',None)
				# print '\n\n*****************************'
				# print comment
				# print '\n\n******************************'
				path = request.POST.get('path','/commonblog/')
				post = CandidatePosts.objects.get(id=candidatepostid)
				if comment != None or comment != '' :
					comment = StudentsComments(student=student,post=post,comment=comment)
					comment.save()
					return HttpResponseRedirect(path)

			else :
				return HttpResponse("<h3>Method must be post for submitting data</h3>")
		
		except Student.DoesNotExist :
			return HttpResponse("<h3>Student does not exist</h3>")

		except CandidatePosts.DoesNotExist :
			return HttpResponse("<h3>Error 404<h3><br>Post Doesnot Exists in the database<br>")
	

	else : 
		return HttpResponse("<h3>You are not authorized to do so </h3>")


@login_required
def deletecomment(request,candidatepostid,commentid):
	link = request.GET.get('link','')
	# print "\n\ndeletecomment view\nlink in get method = ",link, "\n\n"
	# print 
	if request.user.is_authenticated():
		username = request.user.username
		try :
			student = Student.objects.get(username=username)
			post = CandidatePosts.objects.get(id=candidatepostid)
			comment = StudentsComments.objects.get(id=commentid)
			if post == comment.post and comment.student == student :
				comment.delete()
				if link != '':
					return HttpResponseRedirect(link)
				else :
					return HttpResponseRedirect('/candidatesbulletin/')

			else :
				return HttpResponse("<h3>This is not your comment</h3>")

		except Student.DoesNotExist:
			return HttpResponse("<h3>Student does not exist</h3>")
		except CandidatePosts.DoesNotExist:
			return HttpResponse("<h3>Error 404<h3><br>Post Doesnot Exists in the database<br>")
		except StudentsComments.DoesNotExist:
			return HttpResponse("<h3>Error 404<h3><br>Comment Doesnot Exists in the database<br>")

	else:
		return HttpResponse("You are not authorized to do this")

#extra done 

# @login_required
# def add(request):
# 	context = {}
# 	if request.user.is_authenticated():
# 		try:
# 			username = request.user.username
# 			student = Student.objects.get(username=username)
#			context['student'] = student
# 			if student.iscandidate:
# 				candidate = Candidate.objects.get(student=student)
# 				if request.method == "POST":
# 					content = request.POST.get('content','')
# 					if content == '':
# 						return HttpResponseRedirect('/candidatesbulletin/')

# 					candidatepost = CandidatePosts(candidate=candidate, content=content)
# 					candidatepost.save()

# 					return HttpResponseRedirect('/candidatesbulletin/')


# 				else:
# 					return HttpResponse("<h3>You cannot send your sensitive data through get method</h3>")

# 			else:
# 				return HttpResponse("<h3>Only Candidates can add a post</h3>")

# 		except :
# 			return HttpResponse("<h3>You are not authorized to add the post</h3>")
