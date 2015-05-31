from django.shortcuts import render
from ask.models import Question, Answer, Tag, Like, CustomUser
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login as djangoLogin, logout as djangoLogout
from ask.forms import RegisterForm, MainSettingsForm, PswSettingsForm, AvatarSettingsForm, LoginForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required



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
	redirect_to = request.GET.get('next', '/')

	context = {'user':getAuthenticatedUser(request)}
	form = LoginForm()
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.login_user(request):
			return HttpResponseRedirect(redirect_to)
	context.update({'form':form})
	return render(request, 'login.html', context)

def register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	context = ({'user':getAuthenticatedUser(request)})
	form = RegisterForm()

	try:
		path = request.GET['continue']
	except KeyError, e:
		path='/'

	if request.method == 'POST':
		form = RegisterForm(request.POST, request.FILES)
		if form.saveUser():
			return HttpResponseRedirect(path)
		else:
			HttpResponseRedirect('/')

	user = getAuthenticatedUser(request)
	context.update({'user':user, 'form':form})
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

@login_required(login_url='/login/')
def settings(request):
    User = getAuthenticatedUser(request)

    if request.method == 'POST':
        if 'login' in request.POST:
            mainForm = MainSettingsForm(request.POST)

            if mainForm.is_valid_(User):
                User.username = mainForm.cleaned_data.get('login')
                User.email = mainForm.cleaned_data.get('email')
                User.first_name = mainForm.cleaned_data.get('nickName')
                User.save()

            login = request.POST.get('login')
            email = request.POST.get('email')
            nickName = request.POST.get('nickName')
        else:
            login = User.username
            email = User.email
            nickName = User.first_name
            mainForm = MainSettingsForm()

        if 'password1' in request.POST:
            pswForm = PswSettingsForm(request.POST)
            if pswForm.is_valid_():
                User.set_password(pswForm.cleaned_data.get('password1'))
                User.save()
        else:
            pswForm = PswSettingsForm()

        if 'avatar' in request.FILES:
            avatarForm = AvatarSettingsForm(request.POST, request.FILES)
            if avatarForm.is_valid():
                User.avatar = avatarForm.cleaned_data.get('avatar')
                User.save()
        else:
            avatarForm = AvatarSettingsForm()

    else:
        login = User.username
        email = User.email
        nickName = User.first_name
        mainForm = MainSettingsForm()
        pswForm = PswSettingsForm()
        avatarForm = AvatarSettingsForm()

    context = {'user':User, 'mainForm':mainForm, 'pswForm':pswForm, 'avatarForm':avatarForm, 'login':login, 'email':email, 'nickName':nickName}
    return render(request, 'settings.html', context)

