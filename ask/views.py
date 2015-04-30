from django.shortcuts import render
from ask.models import Question, Answer, Tag, Like, CustomUser
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

global_context = {"authorized" : True}

def index(request, order=None):
	context = dict(global_context)

	questions_on_page = 20

	tag = request.GET.get('tag')
	page = request.GET.get('page')

	if tag:
		questions = Question.newest_questions.filter(tags__title__exact=tag)
	else:
		if not order or order == 'newest':
			questions = Question.newest_questions.all()
		elif order == 'best':
			questions = Question.best_questions.all()
		else:
			raise Http404

	paginator = Paginator(questions, questions_on_page)

	try:
		question_list = paginator.page(page)
	except PageNotAnInteger:
		question_list = paginator.page(1)
	except EmptyPage:
		question_list = paginator.page(paginator.num_pages)

	context.update( { 'question_list': question_list } )
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
