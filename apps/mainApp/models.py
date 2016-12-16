from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]')

# Create your models here.
class userManager(models.Manager):
	def register(self, post):
		first = post['first_name']
		alias  = post['alias']
		email = post['email']
		password = post['password']
		passwordCheck = post['passwordCheck']
		errors = []
		userId = 0

		if len(first) < 2:
			errors.append('first name must be longer than 2 characters')

		if len(alias) < 2:
			errors.append('alias name must be longer than 2 characters')

		if len(email) < 1:
			errors.append('email cannot be blank')
		elif not EMAIL_REGEX.match(email):
			errors.append('email not in right format')
		
		if len(password) < 8:
			errors.append('password needs to be grater than 8 characters')

		if password != passwordCheck:
			errors.append('password does not match')


		if not errors:
			emailExist = User.objects.filter(email=email)
			if not emailExist:
				hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
				user = User.objects.create(email=email, first_name= first, alias=alias, password=hashed)
				userId = user.id
			else:
				errors.append('Invalid login')
		
		return [errors, userId]

	def login(self, post):
		email = post['email']
		password = post['password']
		errors = []
		userId = 0
		
		if len(email) < 1:
			errors.append('email cannot be blank!')
		elif not EMAIL_REGEX.match(email):
			errors.append('email not in right format')
		
		if len(password) < 8:
			errors.append('password needs to be grater than 8 characters')
		
		if not errors:
			emailExist = User.objects.filter(email=email)

			if emailExist:
				hashed = emailExist[0].password

				if bcrypt.hashpw(password.encode(), hashed.encode()) == hashed:
					userId = emailExist[0].id
			else:
				errors.append('Invalid login')


		return [errors, userId]

class User(models.Model):
	first_name = models.CharField(max_length=50)
	alias = models.CharField(max_length=50, default="alias")
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = userManager()

######
#
#
#
#


class quoteManager(models.Manager):
	def addQuote(self, post, user_id):
		quote = post['quote']
		author = post['author']
		errors = []

		if len(author) < 3:
			errors.append('author name must be longer than 3 chacacters')

		if len(quote) < 10:
			errors.append('quote must be longer than 10 characters')

		if not errors:
			user = User.objects.filter(id=user_id)
			user = user[0]
			Quote.objects.create(user = user , quote = quote, author= author)
		
		return errors

	def addFav(self, quote_id, user_id):
		quote = Quote.objects.filter(id=quote_id)
		quote = quote[0]
		user = User.objects.filter(id=user_id)
		user = user[0]

		fav = Favorite.objects.create(user = user , quote = quote)
		return fav

class Quote(models.Model):
	quote = models.CharField(max_length=500)
	author = models.CharField(max_length=50)
	user = models.ForeignKey('User')
	created_at = models.DateTimeField(auto_now_add = True)
	objects = quoteManager()

class Favorite(models.Model):
	user = models.ForeignKey('User')
	quote = models.ForeignKey('Quote')
	created_at = models.DateTimeField(auto_now_add = True)
	objects = quoteManager()






