from __future__ import unicode_literals
from django.db import models
import bcrypt

class Validator(object):
	def __init__(self):
		self.error = False
		self.msg = {}
	def emailExist(self, formInput):
		email = formInput
		if User.objects.get(email=email):
			return True
		return False
	## Front+back end validation method. Deprecated
	# def isEmpty(self, form):
	# 	testInput = form['val']
	# 	if len(testInput) < form['len']:
	# 		self.error = True
	# 		self.msg[form['name']] = '{} must be more than {} characters'.format(form['name'].capitalize(), form['len'])
	# 	return [self.error, self.msg]
	# def emailInvalid(self, form):
	# 	email = form['val']
	# 	if not EMAIL_REGEX.match(email):
	# 		self.error = True
	# 		self.msg['emailInvalid'] = 'Invalid email'
	# 	return [self.error, self.msg]

class UserManager(models.Manager):
	def isAdmin(self):
		if User.objects.get(id=request.session['user_id']).userlevel_id == 1:
			return True
		else:
			return False
	def isLoggedIn(self, session):
		if 'user_id' in session:
			return True
		else:
			return False

class Userlevel(models.Model):
	level_name = models.CharField(max_length=45)

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	description = models.TextField(default='None')
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	userlevel= models.ForeignKey(Userlevel)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
	message = models.TextField()
	user = models.ForeignKey(User)
	targetUser = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
	comment = models.TextField()
	message = models.ForeignKey(Message)
	user = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)