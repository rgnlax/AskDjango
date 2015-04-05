from django.shortcuts import render
from django.http import Http404

def index(request):
	#try:
	response = render(request, 'index.html')
	#except Exception, e:
	#	raise Http404
	return response

def question(request):
	#try:
	response = render(request, 'question.html')
	#except Exception, e:
	#	raise Http404
	return response

def login(request):
	#try:
	response = render(request, 'login.html')
	#except Exception, e:
	#	raise Http404
	return response

def register(request):
	#try:
	response = render(request, 'register.html')
	#except Exception, e:
	#	raise Http404
	return response

def ask(request):
	#try:
	response = render(request, 'ask.html')
	#except Exception, e:
	#	raise Http404
	return response