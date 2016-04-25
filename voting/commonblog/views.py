from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .models import CommonBlog
from accounts.models import Student
from accounts.models import Candidate


@login_required
def list(request):
	context = {}
	student = None
	if request.user.is_authenticated():
		username = request.user.username
		try:
			student = Student.objects.get(username=username)
		except Student.DoesNotExist:
			student = None

	if student and student.iscandidate:
		try: 
			candidate = Candidate.objects.get(student=student)
			context['candidate'] = candidate

		except Candidate.DoesNotExist:
			candidate = "Candidate Does Not Exists" 

	posts = CommonBlog.objects.all().order_by('timestamp')
	context['posts'] = posts
	context['student'] = student

	return render(request,'commonblog/commonblog.html',context)


@login_required
def addblog(request):
	if request.user.is_authenticated():
		if request.method == "POST":
			content = request.POST.get('content','')
			content = content.strip().rstrip()
			if content != '':
				username = request.user.username
				try:
					student = Student.objects.get(username=username)
					blog = CommonBlog(student=student,content = content)
					blog.save()
					return HttpResponseRedirect('/commonblog/')
				except Student.DoesNotExist:
					return HttpResponse('<h3>You are not authorized to do so</h3>')
			else :
				return HttpResponseRedirect('/commonblog/')

		else :
			return HttpResponse("<h3>Don't try to change the method from post to get</h3>")

	else:
		return HttpResponse("<h3>You are not authenicated to do so</h3>")



@login_required
def deleteblog(request,postid):
	context = {}
	try :
		post = CommonBlog.objects.get(id=postid)
		if request.user.is_authenticated():
			if post.student.username == request.user.username:
				post.delete()
				return HttpResponseRedirect('/commonblog/')

			else:
				return HttpResponse("<h3>You haven't posted this comment</h3>")

		else : 
			return HttpResponse("<h3>You aren't authorized to delete this comment</h3>")	
	
	except:
		return HttpResponse("<h3>This post doesn't exists.</h3>")			


