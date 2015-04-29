from django.shortcuts import render
from ask.models import Question, Answer, Tag, Like, CustomUser
from django.http import Http404

global_context = {"authorized" : True}

def index(request, order=None):
	tag = request.GET.get('tag')
	context = dict(global_context)
	if tag:
		question_list = Question.newest_questions.filter(tags__title__exact=tag)
	else:
		if not order or order == 'newest':
			question_list = Question.newest_questions.all()
		elif order == 'best':
			question_list = Question.best_questions.all()
		else:
			raise Http404

	context.update( { 'question_list': question_list} )
	context.update( { 'order': order } )
	context.update( { 'tag': tag } )
	response = render(request, 'index.html', context)
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
