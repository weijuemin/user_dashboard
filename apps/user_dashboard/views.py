from django.shortcuts import render, redirect, HttpResponse
from .models import Validator, User, Userlevel, Message, Comment, UserManager
from django.core.urlresolvers import reverse
import bcrypt
# Create your views here.
def index(request):
	return render(request, 'user_dashboard/index.html')
def login(request):
	return render(request, 'user_dashboard/login.html')
def loginProcess(request): # next time put into models
	validator = Validator()
	error = False
	msg = {}
	request.session['email'] = request.POST['email']
	if validator.isEmpty(request.POST, 'email'):
		error = True
		msg['emailErr0'] = 'Please enter email'
	if validator.emailInvalid(request.POST, 'email'):
		error = True
		msg['emailErr1'] = 'Oops! Email invalid'
	if validator.isEmpty(request.POST, 'password'):
		error = True
		msg['pwErr0'] = 'Please enter password'
	if not error:
		if not User.objects.filter(email=request.POST['email']):
			error = True
			msg['existErr'] = 'Email doesn\'t exist. How about register now?'
		else:
			thisUser = User.objects.get(email=request.POST['email'])
			if bcrypt.hashpw(request.POST['password'].encode(encoding='utf-8'), thisUser.password.encode(encoding='utf-8')) == thisUser.password.encode(encoding='utf-8'):
				request.session.pop('email')
				request.session['fname'] = thisUser.first_name
				request.session['lInit'] = thisUser.last_name[:1].capitalize()
				request.session['user_id'] = thisUser.id
				request.session['ul_id'] = thisUser.userlevel.id
				return redirect(reverse('ud_show_dashboard'))
			else:
				error = True
				msg['pwErr1'] = 'Password incorrect!'
	context = {
		'msg': msg,
	}
	return render(request, 'user_dashboard/login.html', context)
def register(request):
	return render(request, 'user_dashboard/register.html')
def registerProcess(request): # next time put into models
	validator = Validator()
	error = False
	msg = {}
	# Only for validation use. Destroy after registered
	request.session['first_name'] = request.POST['first_name']
	request.session['last_name'] = request.POST['last_name']
	request.session['email'] = request.POST['email']
	# end session assignment
	if validator.isEmpty(request.POST, 'first_name'):
		error = True
		msg['fnameErr'] = 'Please enter first name'
	if validator.isEmpty(request.POST, 'last_name'):
		error = True
		msg['lnameErr'] = 'Please enter last name'
	if validator.isEmpty(request.POST, 'email'):
		error = True
		msg['emailErr0'] = 'Please enter email'
	if validator.emailInvalid(request.POST, 'email'):
		error = True
		msg['emailErr1'] = 'Oops! Email invalid'
	if validator.pwIsShort(request.POST, 'password'):
		error = True
		msg['pwErr0'] = 'Password must be more than 8 characters'
	# password match check conducted in jquery - secure since it's local
	if not error:
		if User.objects.filter(email=request.POST['email']):
			error = True
			msg['existErr'] = 'Email already registered. Please log in or use another email'
		else:
			pw_hash = bcrypt.hashpw(request.POST['password'].encode(encoding='utf-8'), bcrypt.gensalt())
			request.session.pop('first_name')
			request.session.pop('last_name')
			request.session.pop('email')
			if not User.objects.all():
				User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash, userlevel_id=1)
			else:
				User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash, userlevel_id=2)
			thisUser = User.objects.get(email=request.POST['email'])
			request.session['fname'] = thisUser.first_name
			request.session['lInit'] = thisUser.last_name[:1].capitalize()
			request.session['user_id'] = thisUser.id
			request.session['ul_id'] = thisUser.userlevel.id
			return redirect(reverse('ud_show_dashboard'))
	context = {
		'msg': msg,
	}
	return render(request, 'user_dashboard/register.html', context)

def showDashboard(request):
	usermanager = UserManager()
	if usermanager.isLoggedIn(request.session):
		users = User.objects.all()
		context = {
			'users': users
		}
		return render(request, 'user_dashboard/dashboard.html', context)
	else:
		return redirect(reverse('ud_login'))
def new(request):
	return render(request, 'user_dashboard/admin_add.html')
def newProcess(request):
	validator = Validator()
	error = False
	msg = {}
	request.session['first_name'] = request.POST['first_name']
	request.session['last_name'] = request.POST['last_name']
	request.session['email'] = request.POST['email']
	if validator.isEmpty(request.POST, 'first_name'):
		error = True
		msg['fnameErr'] = 'Please enter first name'
	if validator.isEmpty(request.POST, 'last_name'):
		error = True
		msg['lnameErr'] = 'Please enter last name'
	if validator.isEmpty(request.POST, 'email'):
		error = True
		msg['emailErr0'] = 'Please enter email'
	if validator.emailInvalid(request.POST, 'email'):
		error = True
		msg['emailErr1'] = 'Oops! Email invalid'
	if 'userlevel_id' not in request.POST:
		error = True
		msg['selectErr'] = 'Please select user level'
	if validator.pwIsShort(request.POST, 'password'):
		error = True
		msg['pwErr0'] = 'Password must be more than 8 characters'
	# password match check conducted in jquery - very secure since it's local
	if not error:
		pw_hash = bcrypt.hashpw(request.POST['password'].encode(encoding='utf-8'), bcrypt.gensalt())
		for skey in ['first_name', 'last_name', 'email']:
			if skey in request.session:
				request.session.pop(skey)
		User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash, userlevel_id=request.POST['userlevel_id'])
		return redirect(reverse('ud_show_dashboard'))
	context = {
		'msg': msg,
	}
	return redirect(reverse('ud_adduser'), context)
def editUser(request):
	thisUser = User.objects.get(id=request.session['user_id'])
	context = {
		'curUser':thisUser
	}
	return render(request, 'user_dashboard/normal_edit.html', context)
def editUserProcess(request):
	pw_hash = bcrypt.hashpw(request.POST['password'].encode(encoding='utf-8'), bcrypt.gensalt())
	User.objects.filter(id=request.session['user_id']).update(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], description=request.POST['description'], password=pw_hash)
	return redirect(reverse('ud_show_dashboard'))
def showUser(request, user_id):
	displayedUser = User.objects.get(id=user_id)
	dUserMsgs = Message.objects.filter(targetUser=user_id)
	idRange = []
	for dmsg in dUserMsgs:
		idRange.append(dmsg.id)
	dUserCmts = Comment.objects.filter(message_id__in=idRange)
	context = {
		'displayedUser': displayedUser,
		'dUserMsgs': dUserMsgs,
		'dUserCmts': dUserCmts
	}
	return render(request, 'user_dashboard/show.html', context)
def removeUser(request, user_id):
	if request.POST['rmOption'] == 'yes':
		User.objects.get(id=user_id).delete()
	return redirect(reverse('ud_show_dashboard'))
def adminEditUser(request, user_id):
	usermanager = UserManager()
	editingUser = User.objects.get(id=user_id)
	if usermanager.isLoggedIn(request.session):
		context = {
			'editingUser': editingUser
		}
		return render(request, 'user_dashboard/admin_edit.html', context)
	else:
		return redirect(reverse('ud_login'))
def adminUpdateUser(request, user_id):
	validator = Validator()
	error = False
	msg = {}
	editingUser = User.objects.filter(id=user_id)
	if validator.isEmpty(request.POST, 'first_name'):
		error = True
		msg['fnameErr'] = 'Please enter first name'
	if validator.isEmpty(request.POST, 'last_name'):
		error = True
		msg['lnameErr'] = 'Please enter last name'
	if validator.isEmpty(request.POST, 'email'):
		error = True
		msg['emailErr0'] = 'Please enter email'
	if 'userlevel_id' not in request.POST:
		error = True
		msg['selectErr'] = 'Please select user level'
	if validator.emailInvalid(request.POST, 'email'):
		error = True
		msg['emailErr1'] = 'Oops! Email invalid'
	if validator.pwIsShort(request.POST, 'password'):
		error = True
		msg['pwErr0'] = 'Password must be more than 8 characters'
	# password match check conducted in jquery - very secure since it's local
	if not error:
		pw_hash = bcrypt.hashpw(request.POST['password'].encode(encoding='utf-8'), bcrypt.gensalt())
		for skey in ['first_name', 'last_name', 'email']:
			if skey in request.session:
				request.session.pop(skey)
		editingUser.update(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash, userlevel_id=request.POST['userlevel_id'])
		return redirect(reverse('ud_show_dashboard'))
	context = {
		'msg': msg,
		'editingUser':editingUser
	}
	return redirect('/dashboard/users/admin/update/{}'.format(user_id), context)
def messageProcess(request, user_id):
	validator = Validator()
	if validator.isEmpty(request.POST, 'msgContent'):
		return redirect('/dashboard/users/show/{}'.format(user_id))
	Message.objects.create(message=request.POST['msgContent'], user_id=request.session['user_id'], targetUser=user_id)
	return redirect('/dashboard/users/show/{}'.format(user_id))
def commentProcess(request, user_id, msg_id):
	validator = Validator()
	if validator.isEmpty(request.POST, 'cmtContent'):
		return redirect('/dashboard/users/show/{}'.format(user_id))
	Comment.objects.create(comment=request.POST['cmtContent'], user_id=request.session['user_id'], message_id=msg_id)
	return redirect('/dashboard/users/show/{}'.format(user_id))
def logout(request):
	usermanager = UserManager()
	usermanager.logout(request.session)
	return redirect(reverse('ud_index'))

# For first time setup. Should be moved to models as manager method	
# def privateUserlevel(request):
# 	Userlevel.objects.create(level_name='admin')
# 	Userlevel.objects.create(level_name='normal')
# 	userlevels = Userlevel.objects.all()
# 	for ul in userlevels:
# 		print (ul.id, ul.level_name)
# 	return HttpResponse("you've changed userlevel name")