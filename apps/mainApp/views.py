from django.shortcuts import render, redirect
from . import models
from django.contrib import messages

# Create your views here.


def index(request):
	return render(request, 'mainApp/index.html')

def newUser(request):
	res = models.User.objects.register(request.POST)
	message = "registered"
	return processSignon(request, res, message)

def signOn(request):
	res = models.User.objects.login(request.POST)
	message = "logged on"
	return processSignon(request, res, message)

def processSignon(request, res, message):	
	if not res[0]:
		messages.success(request, "You have successfully {}!!!!".format(message))
		request.session['id'] = res[1]
		return redirect('/success')

	for error in res[0]:
		messages.warning(request, error)
	return redirect('/')

def success(request):
	if request.session.get('id'):
		favId = []

		userInfo = models.User.objects.filter(id = request.session['id'])

		favs = models.Favorite.objects.filter(user__id = request.session['id']).order_by('-created_at')
		for fav in favs:
			favId.append(fav.quote.id)
		quotes = models.Quote.objects.all().exclude(id__in = favId).order_by('-created_at')

		data = {"user":userInfo[0], "quotes": quotes, "favs":favs}
		return render(request, "mainApp/success.html", data)
	return redirect('/')

def add_quote(request):
	response = models.Quote.objects.addQuote(request.POST, request.session['id'])
	if not response:
		return redirect('/success')
	
	for error in response:
		messages.warning(request, error)
	return redirect('/success')

def add_to_fav(request, id):
	models.Quote.objects.addFav(id, request.session['id'])
	return redirect('/success')

def remove_fav(request, id):
	delThis = models.Favorite.objects.filter(id = id).delete()
	return redirect('/success')

def user_page(request, id):
	quotes = models.Quote.objects.filter(user__id = id)
	userInfo = models.User.objects.filter(id = id)

	data = {"quotes":quotes, "user": userInfo[0]}
	return render(request, 'mainApp/user_page.html', data)

def logout(request):
	request.session.clear()
	return redirect('/')
