from django.shortcuts import render
from ask.models import Question, Answer, Tag, Like, CustomUser
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login as djangoLogin, logout as djangoLogout
from ask.forms import RegisterForm, MainSettingsForm, PswSettingsForm, AvatarSettingsForm, LoginForm, QuestionForm, AnswerForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import datetime



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
		question_ = Question.objects.get(pk=question_id)
	except ObjectDoesNotExist:
		raise Http404

	user = getAuthenticatedUser(request)

	if user:
		if request.method == 'POST':
			form = AnswerForm(request.POST)
			if form.is_valid():
				answ = Answer.objects.create(
					author=user, 
					content=form.cleaned_data.get('content'), 
					created=datetime.now(), 
					question=question_ 
					)
				answ.save()

	answers_on_page = 10
	answers = question_.answer_set.order_by('-rating', '-created')

	page = request.GET.get('page')
	paginator = Paginator(answers, answers_on_page)

	try:
		answer_list = paginator.page(page)
	except PageNotAnInteger:
		answer_list = paginator.page(1)
	except EmptyPage:
		answer_list = paginator.page(paginator.num_pages)

	context = {'user':user}
	context.update( { 'question': question_} )
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

@login_required(login_url='/login/')
def ask(request):
	user = getAuthenticatedUser(request)
	context = {'user':user}
	form = QuestionForm()
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			question = Question.objects.create(
				author=user, 
				title=form.cleaned_data.get('title'), 
				content=form.cleaned_data.get('content'), 
				created=datetime.now()
				)
			tags = form.cleaned_data.get('tags').split(',')
			for tag in tags:
				try:
					if ' ' in tag:
						tag = tag.replace(' ', '_')
					t = Tag.objects.get(title=tag)
				except Tag.DoesNotExist:
					t = Tag.objects.create(title=tag)
					t.save()
				question.tags.add(t)
			question.save()
			return HttpResponseRedirect('/question/' + str(question.id))
	context.update({'form':form})
	return render(request, 'ask.html', context)


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

def like(request):
    if request.method == 'POST':
        response_data = {}

        user = getAuthenticatedUser(request)

        object_id = int(request.POST.get('object_id',''))
        like_type = int(request.POST.get('like_type',''))
        object_type = request.POST.get('object_type','')

        if user:
            new_rating = None
            error = None

            if object_type == 'answer':
                answ = Answer.objects.get(id=object_id)

                if user != answ.author:
                    try:
                        like = Like.objects.filter(answer__id=object_id).get(author=user)
                        var = setRatingVar(like_type, int(like.value))
                        like.value = like_type
                        like.save()
                    except:
                        like = Like.objects.create(author=user, value=like_type)
                        like.save()
                        answ.likes.add(like)
                        var = like_type

                    answ.rating = str(var + answ.rating)
                    answ.save()
                    new_rating = answ.rating
                    result = 'Create like successful!'
                else:
                    result = 'Like wasn\'t created!'
                    error = 'It is your answer!'

            elif object_type == 'question':
                quest = Question.objects.get(id=object_id)

                if user != quest.author:
                    try:
                        like = Like.objects.filter(question__id=object_id).get(author=user)
                        var = setRatingVar(like_type, int(like.value))
                        like.value = like_type
                        like.save()
                    except:
                        like = Like.objects.create(author=user, value=like_type)
                        like.save()
                        quest.likes.add(like)
                        var = like_type

                    quest.rating = str(var + quest.rating)
                    quest.save()
                    new_rating = quest.rating
                    result = 'Create like successful!'
                else:
                    result = 'Like wasn\'t created!'
                    error = 'It is your question!'

            else:
                result = 'Like wasn\'t created!'
                error = 'Object not found!'

            response_data['result'] = result
            if new_rating:
                response_data['new_rating'] = new_rating
            if error:
                response_data['error'] = error

        else:
            response_data['result'] = 'Like wasn\'t created!'
            response_data['error'] = 'User is not authenticated!'

        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "No POST data!"})

def setRatingVar(like_type, last_type):
    if last_type == -1:
        if like_type == -1:
            var = 0
        else:
            var = like_type + 1
    elif last_type == 1:
        if like_type == 1:
            var = 0
        else:
            var = like_type - 1
    else:
        var = like_type
    return var


def set_correct(request):
    if request.method == 'POST':
        response_data = {}

        user = getAuthenticatedUser(request)

        answer_id = int(request.POST.get('answer_id',''))

        if user:
            answ = Answer.objects.get(id=answer_id)

            if user == answ.question.author:
                answ.correct =  not answ.correct
                answ.save()
                result = 'Set correct successful!'
            else:
                result = 'Set correct wasn\'t checked!'
                response_data['error'] = 'This question isn\'t your!'

            response_data['result'] = result
            response_data['new_state'] = answ.correct
        else:
            response_data['result'] = 'Set correct wasn\'t checked!'
            response_data['error'] = 'User is not authenticated!'

        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "No POST data!"})

