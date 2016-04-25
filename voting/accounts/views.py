import re
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Student
from .models import Candidate
from django.contrib import messages


def index(request):
	return render(request,'accounts/demo.html')



def login(request):
	return render(request,'accounts/login.html')


def auth_view(request):
	next = request.GET.get('next','/commonblog/')
	# print "\n\n\nnext = ", next,"\n\n\n\n"
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		if username.endswith('@iitp.ac.in'):
			username = username[:-11]


		if username == 'prince':
			user = auth.authenticate(username=username,password=password)

			if user is not None:
				auth.login(request,user)
				return HttpResponseRedirect('/administrator/')	

		if username != '':
			username = username.lower()
		user = auth.authenticate(username=username,password=password)


		if user is not None :
			auth.login(request,user)
			return HttpResponseRedirect(next)
		else :
			context = {}
			context['error_login'] = 'Invalid email or password'
			return render(request,'accounts/login.html',context)

	else :
		return HttpResponse("Something bad happened")


# @login_required
# def loggedin(request):
# 	return render(request,'accounts/loggedin.html')


@login_required
def myprofile(request):
	context = {}
	try : 
		if request.user.is_authenticated():
			student = Student.objects.get(username=request.user.username)
			context['student'] = student
			return render(request,'accounts/profile.html',context)
		else :
			context['error_login'] = 'You are not authorized to view this page'
			return render(request,'accounts/profile.html',context)

	except : 
		context['error_authorization'] = 'You are not authorized to view this page'
		return render(request,'accounts/profile.html',context)



@login_required
def updateprofile(request):
	context = {}
	error = []
	try:
		if request.user.is_authenticated():
			student = Student.objects.get(username=request.user.username)
			if request.method == 'POST':
				firstname = request.POST.get('firstname')
				lastname = request.POST.get('lastname')
				gender = request.POST.get('gender')
				program = request.POST.get('program')
				department = request.POST.get('department')
				year = request.POST.get('year')

				if firstname == '':
					firstname = student.firstname
				if lastname == '' : 
					lastname = student.lastname
				if not gender or gender == '':
					gender = student.gender
				if not program or program == '' :
					program = student.program
				if department == '' :
					department = student.department
				if year == '':
					year = student.year

				firstname , lastname = validate_name(firstname,lastname)
				gender = validate_gender(gender)
				program = validate_program(program)
				department = validate_department(department)
				year = validate_year(program,year)

				if firstname is None or lastname is None :
					context['error_name'] = '* Invalid firstname or lastname. Use only characters or whitespaces'
					errors.append(None)

				if gender is None :
					context['error_gender'] = '* Gender must be male or female'
					errors.append(None)

				if program is None :
					context['error_program'] = '* Program must be either B.Tech M.Tech or Phd'
					errors.append(None)

				if department is None :
					context['error_department'] = '* Department is invalid'
					errors.append(None)

				if year is None :
					context['error_year'] = '* Year is invalid'
					errors.append(None)

				for error in errors :
					if error is None : 
						return render(request,'accounts/profile.html',context)


				student.firstname = firstname
				student.lastname = lastname
				student.gender = gender
				student.program = program
				student.department = department
				student.year = year
				student.save()

				context['updated'] = 'Profile Updated Successfully'
				return render(request,'accouts/profile.html',context)


	except:
		return HttpResponse("You are not allowed to do so")
			


@login_required
def changepassword(request):
	return render(request,'accounts/changepassword.html')
	


@login_required
def updatepassword(request):
	context = {}

	if request.user.is_authenticated():
		if request.method == "POST":
			currentpassword = request.POST.get('currentpassword','')
			newpassword = request.POST.get('newpassword','')
			newconfirmpassword = request.POST.get('newconfirmpassword','')

			user = auth.authenticate(username=username,password=currentpassword)
			if user is not None:
				if newpassword != newconfirmpassword :
					context['error_password'] = "*Passwords don't match"
					return render(request,'accounts/changepassword.html',context)

				password = validate_password(newpassword,newconfirmpassword)
				if password is None:
					context['error_password'] = "*Passwords don't match"
					return render(request,'accounts/changepassword.html',context)

				if password == "small":
					context['error_password'] = "*Passwords must be 6 characters long"
					return render(request,'accounts/changepassword.html',context)

				else:
					context['updated_password'] = 'Password Successfuly Updated'
					return render(request,'accounts/changepassword.html',context)

			else :
				context['error_currentpassword'] = '*Current Password entered is not correct'
				return render(request,'accounts/changepassword.html',context)

	else :
		return HttpResponse("You are not authenticated.")



def logout(request):
	auth.logout(request)
	messages.success(request, "Successfully logged out")
	return HttpResponseRedirect('/accounts/login/')


def register(request):
	return render(request,'accounts/register.html')



def candidatelist(request):
	candidates = Candidate.objects.all()
	context = {}
	# context['general_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='General Secretary').order_by('student__username')
	# context['cultural_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Cultural Secretary').order_by('student__username')
	# context['technical_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Technical Secretary').order_by('student__username')
	# context['sports_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Sports Secretary').order_by('student__username')
	# context['environmental_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True, postname='Environmental Secretary').order_by('student__username')
	# context['mess_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Mess Secretary').order_by('student__username')
	# context['maintenance_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Maintenance Secretary').order_by('student__username')
	# context['literary_sec'] = Candidate.objects.filter(student__year=year,student__iscandidate=True,postname='Literary Secretary').order_by('student__username')
	# context['candidates'] = candidates
	context['general_sec_I'] = candidates.filter(student__year='I',postname='General Secretary')
	context['general_sec_II'] = candidates.filter(student__year='II',postname='General Secretary')
	context['general_sec_III'] = candidates.filter(student__year='III',postname='General Secretary')
	context['general_sec_IV'] = candidates.filter(student__year='IV',postname='General Secretary')

	context['cultural_sec_I'] = candidates.filter(student__year='I',postname='Cultural Secretary')
	context['cultural_sec_II'] = candidates.filter(student__year='II',postname='Cultural Secretary')
	context['cultural_sec_III'] = candidates.filter(student__year='III',postname='Cultural Secretary')
	context['cultural_sec_IV'] = candidates.filter(student__year='IV',postname='Cultural Secretary')


	context['technical_sec_I'] = candidates.filter(student__year='I',postname='Technical Secretary')
	context['technical_sec_II'] = candidates.filter(student__year='II',postname='Technical Secretary')
	context['technical_sec_III'] = candidates.filter(student__year='III',postname='Technical Secretary')
	context['technical_sec_IV'] = candidates.filter(student__year='IV',postname='Technical Secretary')


	context['sports_sec_I'] = candidates.filter(student__year='I',postname='Sports Secretary')
	context['sports_sec_II'] = candidates.filter(student__year='II',postname='Sports Secretary')
	context['sports_sec_III'] = candidates.filter(student__year='III',postname='Sports Secretary')
	context['sports_sec_IV'] = candidates.filter(student__year='IV',postname='Sports Secretary')


	context['environmental_sec_I'] = candidates.filter(student__year='I',postname='Environmental Secretary')
	context['environmental_sec_II'] = candidates.filter(student__year='II',postname='Environmental Secretary')
	context['environmental_sec_III'] = candidates.filter(student__year='III',postname='Environmental Secretary')
	context['environmental_sec_IV'] = candidates.filter(student__year='IV',postname='Environmental Secretary')


	context['mess_sec_I'] = candidates.filter(student__year='I',postname='Mess Secretary')
	context['mess_sec_II'] = candidates.filter(student__year='II',postname='Mess Secretary')
	context['mess_sec_III'] = candidates.filter(student__year='III',postname='Mess Secretary')
	context['mess_sec_IV'] = candidates.filter(student__year='IV',postname='Mess Secretary')


	context['maintenance_sec_I'] = candidates.filter(student__year='I',postname='Mess Secretary')
	context['maintenance_sec_II'] = candidates.filter(student__year='II',postname='Mess Secretary')
	context['maintenance_sec_III'] = candidates.filter(student__year='III',postname='Mess Secretary')
	context['maintenance_sec_IV'] = candidates.filter(student__year='IV',postname='Mess Secretary')


	context['literary_sec_I'] = candidates.filter(student__year='I',postname='Literary Secretary')
	context['literary_sec_II'] = candidates.filter(student__year='II',postname='Literary Secretary')
	context['literary_sec_III'] = candidates.filter(student__year='III',postname='Literary Secretary')
	context['literary_sec_IV'] = candidates.filter(student__year='IV',postname='Literary Secretary')



	return render(request,'accounts/candidatelist.html',context)



def register_result(request):
	context = {}
	errors = []

	if request.method == 'POST':
		firstname = request.POST.get('firstname')
		lastname = request.POST.get('lastname')
		rollno = request.POST.get('rollno')
		email = request.POST.get('email','')
		gender = request.POST.get('gender','')
		program = request.POST.get('program','')
		department = request.POST.get('department')
		year = request.POST.get('year')
		password = request.POST.get('password')
		confirmpassword = request.POST.get('confirmpassword')
		
		
		email = email.strip().rstrip()
		rollno = rollno.strip().rstrip()
		firstname = firstname.strip().rstrip()
		lastname = lastname.strip().rstrip()

		if email == '':

			context['error_email'] = '* Email should be vaild IITP email'
			errors.append(None)
		else:
			if email.endswith('@iitp.ac.in'):
				username = email.lower()[:-11]
			else:
				username = email.lower()
				email = email.lower() + '@iitp.ac.in'


		if firstname == '' or lastname == '':
			context['error_name'] = '*Firstname and lastname cannot be empty'
			errors.append(None)
		else:
			firstname, lastname = validate_name(firstname,lastname)

		if rollno == '' :
			context['error_rollno'] = '* Rollno cannot be empty'
			errors.append(None)
		else:
			rollno = validate_rollno(rollno)

		if email == '':
			context['error_email'] = '* Email cannot be empty'
			errors.append(None)
		else:
			email = validate_email(email)

		if not gender or gender == '':	
			context['error_gender'] = '* Gender cannot be empty'
			# print "error in gender"
			errors.append(None)
		else:
			gender = validate_gender(gender)

		if not program or program == '':
			context['error_program'] = '* Program cannot be empty'
			flag = 0
			errors.append(None)
		else:
			program = validate_program(program)
			flag = 1
		
		if department == 'blank' or department == '':
			context['error_department'] = '* Department cannot be empty'
			errors.append(None)
		else:
			department = validate_department(department)
		
		if year == 'blank' or year == '':
			context['error_year'] = '* Year cannot be empty'
			errors.append(None)
		elif flag == 0:
			context['error_year'] = '* Program must be correct first to check year'
			errors.append(None)
		else : 
			year = validate_year(program,year)

		if password == '' or confirmpassword == '':
			context['error_password'] = "* Passwords cannot be empty"
			errors.append(None)
		else:
			password = validate_password(password,confirmpassword)

		if firstname is None or lastname is None :
			context['error_name'] = '* Invalid firstname or lastname. Use only characters or whitespaces'
			errors.append(None)

		if rollno is None : 
			context['error_rollno'] = '* This should be valid IITP Roll No'
			errors.append(None)

		if email is None :
			print "\n\nemail is none\n\n"
			context['error_email'] = '* Email should be vaild IITP email'
			errors.append(None)

		if gender is None :
			context['error_gender'] = '* Gender must be male or female'
			errors.append(None)

		if program is None :
			context['error_program'] = '* Program must be either B.Tech M.Tech or Phd'
			errors.append(None)

		if department is None :
			context['error_department'] = '* Department is invalid'
			errors.append(None)

		if year is None :
			context['error_year'] = '* Year is invalid'
			errors.append(None)

		if password is None :
			context['error_password'] = "* Passwords don't match"
			errors.append(None)
			print "return value is None\n\n\n"

		if password == "small":
			print "return value is small\n\n\n"
			context['error_password'] = "* Passwords is too small"
			errors.append(None)

		for error in errors :
			if error is None : 
				return render(request,'accounts/register.html',context)


		try : 
			student = Student.objects.get(username=username)
			context = {}
			if student is not None:
				context['email_exists'] = '* Email already registered' 
			return render(request,'accounts/register.html',context)

		except Student.DoesNotExist:	
			user = User.objects.create_user(username=username,password=password)
			user.save()
			department = department.upper()
			student = Student(username=username,firstname=firstname,lastname=lastname,rollno=rollno,\
				email=email,gender=gender,program=program,department=department,year=year)
			student.save()

			messages.success(request, "Successfully Registered")
			return HttpResponseRedirect('/accounts/login')

	else:
		return HttpResponse("Something wrong has been tried.")



@login_required
def applyforcandidate(request):
	context = {}
	if request.user.is_authenticated():
		try:
			username = request.user.username
			student = Student.objects.get(username=username)
			context['student'] = student
			if not student.iscandidate:	
				return render(request,'accounts/applyforcandidate.html',context)
			else:
				return HttpResponse("<h3>You are already a candidate</h3>")
		except:
			return HttpResponse("<h3>No student with current username exists in database</h3>")
	else:
		return HttpResponse("<h3>You are not authorized to become candidate</h3>")



# incomplete
@login_required
def candidateapplicationresult(request):
	context = {}
	errors = []
	if request.user.is_authenticated():
		try:
			username = request.user.username
			student = Student.objects.get(username=username)
			context['student'] = student
			if not student.iscandidate: 
				if request.method == "POST":
					momento = request.POST.get('momento','')
					competingpost = request.POST.get('post','')

					# print competingpost
					print
					print momento
					print
					print 

					if competingpost == '': 
						context['error_post'] = "* You must choose a post"
						errors.append(None)
					else:
						competingpost = validate_post(competingpost)

					if momento:
						momento = momento.strip().rstrip()

					if momento == '' or len(momento) == 0 or momento == '\t\t':
						context['error_momento'] = "* You must enter your momento"
						errors.append(None)


					if competingpost is None:
						context['error_post'] = "*You must select a valid post. Page is edited"
						errors.append(None)

					for error in errors:
						if error is None:
							return render(request,'accounts/applyforcandidate.html',context)


					competingpost = (competingpost.strip() + " secretary").title()
					student.iscandidate = True
					student.save()
					candidate = Candidate(student=student,momento=momento,postname=competingpost)
					candidate.save()


					return  HttpResponseRedirect('/commonblog/')

				else :
					return HttpResponse("<h3>Method for submission must be POST</h3>")

			else : 
				return HttpResponse("<h3>The student is already a candidate</h3>")

		except Student.DoesNotExist: 
			return HttpResponse("<h3>Username doesnot exists in the database</h3>")

	else : 
		return HttpResponse("<h3>You are not authorized to apply for candidate </h3>")



def validate_post(post):
	''' General Cultural Technical Sports Environment Literary Mess Maintenance '''
	POSTS = ['general','cultural','technical','sports','environmental','mess','maintenance','literary']

	if post != '':
		post = post.lower()
	
	if post in POSTS:
		return post

	else :
		return None



def validate_name(firstname,lastname):
	firstname = firstname.strip().rstrip().title()
	firstname = re.match('^([a-zA-Z]|[\s]|\.|)+$',firstname)
	if firstname is None :
		return None, None
	lastname = lastname.strip().rstrip().title()
	lastname = re.match('^([a-zA-Z]|\.|)+$',lastname)

	if lastname is None:
		return None, None
	else :
		return firstname.group(), lastname.group()



def validate_rollno(rollno):
	''' 4 digits 2/3 characeters 2 digits'''
	temp = re.match('^\d{4}[a-zA-Z]{2,3}\d{2}$',rollno)
	if temp is None :
		return None
	else : 
		return temp.group()


def validate_email(email):
	''' characters . 2/3 characters 2 digits @iitp.ac.in'''
	temp = re.match('^(([a-z]+)|([A-Z]+)).[a-zA-Z]{2,4}[0-9]{2}@iitp.ac.in$',email)
	if temp is None :
		return None
	else : 
		return temp.group()


def validate_gender(gender):
	gender = gender.lower().strip().rstrip()
	# print gender
	if gender == 'male':
		return 'male'
	elif gender == 'female':
		return 'female'
	else : 
		return None


def validate_program(program):
	program = program.lower()
	if program in ['b.tech','m.tech','phd']:
		return program
	else :
		return None



def validate_department(department):
	''' 3 characters '''
	department = re.match('^[a-zA-Z]{2,3}$',department)
	if department is None:
		return None
	else :
		return department.group()


def validate_year(program,year):
	year = year.upper()
	program = program.lower()
	if program in ['b.tech'] and year in ['I','II','III','IV']:
		return year
	elif program in ['m.tech'] and year in ['I','II']:
		return year
	elif program in ['phd'] and year in ['I','II','III','IV' , 'V']:
		return year
	else :
		return None


def validate_password(password,confirmpassword):
	if password == confirmpassword:
		if len(password) < 8:
			return "small"
		else :
			return password
	else :
		return None





