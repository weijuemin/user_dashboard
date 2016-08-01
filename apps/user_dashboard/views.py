from django.shortcuts import render, redirect, HttpResponse
from .models import Validator, User, Userlevel, Message, Comment, UserManager
from django.core.urlresolvers import reverse
import bcrypt
import json
# Create your views here.
def index(request):
	return render(request, 'user_dashboard/index.html')
def login(request):
	return render(request, 'user_dashboard/login.html')

# Front+back end validation method. Deprecated
# def validate(request):
# 	if request.method != 'POST':
# 		return redirect('ud_login')
# 	result = json.loads(request.body)
# 	print result
# 	validator = Validator()
# 	validator.isEmpty(result)
# 	if result['name'] == 'email':
# 		validator.emailInvalid(result)
# 	print validator.error
# 	if not validator.error:
# 		return HttpResponse('')
# 	context = {
# 		'errMsg': validator.msg
# 	}
# 	for key,val in validator.msg.iteritems():
# 		print "{}: {}".format(key, val)
# 	return render(request, 'user_dashboard/validation.html', context)


def loginProcess(request): # next time put into models
	msg = {}
	request.session['email'] = request.POST['email']
	thisUser = User.objects.filter(email=request.POST['email'])
	if not thisUser:
		msg['existErr'] = 'Email doesn\'t exist. Please register first.'
	else:
		thisUser = thisUser[0]
		if bcrypt.hashpw(request.POST['password'].encode(encoding='utf-8'), thisUser.password.encode(encoding='utf-8')) == thisUser.password.encode(encoding='utf-8'):
			request.session.pop('email')
			request.session['fname'] = thisUser.first_name
			request.session['lInit'] = thisUser.last_name[:1].capitalize()
			request.session['user_id'] = thisUser.id
			request.session['ul_id'] = thisUser.userlevel.id
			return redirect('ud_show_dashboard')
		else:
			error = True
			msg['pwErr'] = 'Password incorrect!'
	context = {
		'msg': msg,
	}
	return redirect('ud_login', context)
def register(request):
	return render(request, 'user_dashboard/register.html')
def registerProcess(request): # next time put into models
	msg = {}
	request.session['first_name'] = request.POST['first_name']
	request.session['last_name'] = request.POST['last_name']
	request.session['email'] = request.POST['email']
	if User.objects.filter(email=request.POST['email']):
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
		return redirect('ud_show_dashboard')
	context = {
		'msg': msg,
	}
	return render(request, 'user_dashboard/register.html', context)

def showDashboard(request):
	if 'user_id' not in request.session:
		return redirect('ud_login')
	usermanager = UserManager()
	if usermanager.isLoggedIn(request.session):
		users = User.objects.all()
		context = {
			'users': users
		}
		return render(request, 'user_dashboard/dashboard.html', context)
	else:
		return redirect('ud_login')
def new(request):
	if 'user_id' not in request.session:
		return redirect('ud_login')
	return render(request, 'user_dashboard/admin_add.html')
def newProcess(request):
	if 'user_id' not in request.session:
		return redirect('ud_login')
	msg = {}
	request.session['first_name'] = request.POST['first_name']
	request.session['last_name'] = request.POST['last_name']
	request.session['email'] = request.POST['email']
	if 'userlevel_id' not in request.POST:
		userlevel_id = 2
	else:
		userlevel_id = request.POST['userlevel_id']
	if User.objects.filter(email=request.POST['email']):
		msg['existErr'] = "Email already registered. Please try another email."
		context = {
			'msg': msg,
		}
		return redirect(reverse('ud_adduser'), context)
	for skey in ['first_name', 'last_name', 'email']:
		if skey in request.session:
			request.session.pop(skey)
	pw_hash = bcrypt.hashpw(request.POST['password'].encode(encoding='utf-8'), bcrypt.gensalt())
	User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash, userlevel_id=userlevel_id)
	return redirect('ud_show_dashboard')
def editUser(request):
	if 'user_id' not in request.session:
		return redirect('ud_login')
	thisUser = User.objects.get(id=request.session['user_id'])
	context = {
		'curUser':thisUser
	}
	return render(request, 'user_dashboard/normal_edit.html', context)
def editUserProcess(request):
	if 'user_id' not in request.session:
		return redirect('ud_login')
	pw_hash = bcrypt.hashpw(request.POST['password'].encode(encoding='utf-8'), bcrypt.gensalt())
	User.objects.filter(id=request.session['user_id']).update(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], description=request.POST['description'], password=pw_hash)
	return redirect('ud_show_dashboard')
def showUser(request, user_id):
	if 'user_id' not in request.session:
		return redirect('ud_login')
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
	if 'user_id' not in request.session:
		return redirect('ud_login')
	if request.POST['rmOption'] == 'yes':
		User.objects.get(id=user_id).delete()
	return redirect('ud_show_dashboard')
def adminEditUser(request, user_id):
	if 'user_id' not in request.session:
		return redirect('ud_login')
	usermanager = UserManager()
	editingUser = User.objects.get(id=user_id)
	if usermanager.isLoggedIn(request.session):
		context = {
			'editingUser': editingUser
		}
		return render(request, 'user_dashboard/admin_edit.html', context)
	else:
		return redirect('ud_login')
def adminUpdateUser(request, user_id):
	if 'user_id' not in request.session:
		return redirect('ud_login')
	msg = {}
	editingUser = User.objects.filter(id=user_id)
	if 'userlevel_id' not in request.POST:
		userlevel_id = editingUser[0].userlevel_id
	else:
		userlevel_id = request.POST['userlevel_id']
	pw_hash = bcrypt.hashpw(request.POST['password'].encode(encoding='utf-8'), bcrypt.gensalt())
	for skey in ['first_name', 'last_name', 'email']:
		if skey in request.session:
			request.session.pop(skey)
	editingUser.update(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash, userlevel_id=userlevel_id)
	return redirect('ud_show_dashboard')
def messageProcess(request, user_id):
	if 'user_id' not in request.session:
		return redirect('ud_login')
	Message.objects.create(message=request.POST['msgContent'], user_id=request.session['user_id'], targetUser=user_id)
	return redirect('/dashboard/users/show/{}'.format(user_id))
def commentProcess(request, user_id, msg_id):
	if 'user_id' not in request.session:
		return redirect('ud_login')
	Comment.objects.create(comment=request.POST['cmtContent'], user_id=request.session['user_id'], message_id=msg_id)
	return redirect('/dashboard/users/show/{}'.format(user_id))
def logout(request):
	request.session.clear()
	return redirect('ud_index')

# For first time setup. Should be moved to models as manager method	
# def privateUserlevel(request):
# 	Userlevel.objects.create(level_name='admin')
# 	Userlevel.objects.create(level_name='normal')
# 	userlevels = Userlevel.objects.all()
# 	for ul in userlevels:
# 		print (ul.id, ul.level_name)
# 	return HttpResponse("you've changed userlevel name")