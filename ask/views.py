from django.shortcuts import render
from ask.models import Question, Answer, Tag, Like, CustomUser
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login as djangoLogin, logout as djangoLogout
from forms import  RegisterForm
from django.views.decorators.csrf import csrf_exempt


def index(request, order=None):
	context = {}
	context.update({'user':getAuthenticatedUser(request)})
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

	answers_on_page = 10
	answers = question.answer_set.order_by('-rating', '-created')

	page = request.GET.get('page')
	paginator = Paginator(answers, answers_on_page)

	try:
		answer_list = paginator.page(page)
	except PageNotAnInteger:
		answer_list = paginator.page(1)
	except EmptyPage:
		answer_list = paginator.page(paginator.num_pages)

	context = {}
	context.update({'user':getAuthenticatedUser(request)})
	context.update( { 'question': question} )
	context.update( { 'answer_list': answer_list } )

	response = render(request, 'question.html', context)
	return response

def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')

	context = {'user':getAuthenticatedUser(request)}
	try:
		path = request.GET['continue']
	except KeyError, e:
		path='/'

	try:
		username = request.POST['username']
		password = request.POST['password']
		context.update({'username':username, 'password':password})
	except KeyError:
		pass
	try:
		user = authenticate(username=username, password=password)
	except:
		user = None

	if user is not None:
		if user.is_active:
			djangoLogin(request, user)
			return HttpResponseRedirect(path)
        else:
        	pass
        	#diabled account message
	return render(request, 'login.html', context)

def register(request):
	form = RegisterForm()

	try:
		path = request.GET['continue']
	except KeyError, e:
		path='/'

	if request.method == 'POST':
		form = RegisterForm(request.POST, request.FILES)
		if form.saveUser():
			user = authenticate(username=login, password=password)
			djangoLogin(request, user)
			return HttpResponseRedirect(continue_path)
			
	user = getAuthenticatedUser(request)
	context = {'User':user, 'form':form}
	return render(request, 'register.html', context)

def ask(request):
	#try:
	context.update({'user':getAuthenticatedUser(request)})
	response = render(request, 'ask.html')
	#except Exception, e:
	#	raise Http404
	return response

def getAuthenticatedUser(request):
	if request.user.is_authenticated():
		user = CustomUser.objects.get(user_ptr_id=request.user.id)
	else:
		user = None
	return user

def logout(request):
	djangoLogout(request)
	return HttpResponseRedirect('/')

