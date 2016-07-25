from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# Create your models here.
class Validator(object):
	def isEmpty(self, form, inputName):
		testInput = form[inputName]
		if len(testInput) < 1:
			return True
		else:
			return False
	def emailInvalid(self, form, inputName):
		email = form[inputName]
		if not EMAIL_REGEX.match(email):
			return True
		else:
			return False
	def pwIsShort(self, form, inputName):
		testInput = form[inputName]
		if len(testInput) < 8:
			return True
		else:
			return False

class UserManager(models.Manager):
	def isAdmin(self):
		if User.objects.get(id=request.session['user_id']).userlevel_id == 1:
			return True
		else:
			return False
	def logout(self, session):
		keyList = ['first_name','last_name','fname','lInit','email','user_id','ul_id']
		for key in keyList:
			if key in session:
				session.pop(key)
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