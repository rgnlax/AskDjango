from django.shortcuts import render
from ask.models import Question, Answer, Tag, Like, CustomUser
from django.http import Http404

global_context = {"authorized" : True}

def index(request):
	#try:
	question_list = Question.objects.order_by('created')[:20]
	context = dict(global_context)
	context.update( { 'question_list': question_list } )
	response = render(request, 'index.html', context)
	#except Exception, e:
	#	raise Http404
	return response

def question(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
	except ObjectDoesNotExist:
		raise Http404

	answer_list = question.answer_set.order_by('-created', '-rating')
	context = dict(global_context)
	context.update( { 'question': question} )
	context.update( { 'answer_list': answer_list } )

	response = render(request, 'question.html', context)
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
