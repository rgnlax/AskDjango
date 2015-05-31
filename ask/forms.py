# coding=utf-8
from django import forms
from django.contrib import auth
from models import CustomUser

class LoginForm(forms.Form):
    login = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)
    def login_user(self, request):
        if self.is_valid():
            user = auth.authenticate(username=self.cleaned_data.get('login'), password=self.cleaned_data.get('password'))
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return True
                else:
                    self.add_error(None, 'Ваш аккаунт заблокирован')
            else:
                self.add_error(None, 'Ошибка логина/пароля. Вам в доступе отказано!')
        return False

class RegisterForm(forms.Form):
    login = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=30)
    nickName = forms.CharField(max_length=30)
    password1 = forms.CharField(max_length=30)
    password2 = forms.CharField(max_length=30)
    avatar = forms.ImageField()

    def is_valid_(self):
        ret = self.is_valid()
        if len(CustomUser.objects.filter(username=self.cleaned_data.get('login'))) > 0:
            self.add_error('login', "Это имя уже занято")
            ret = False
        if len(CustomUser.objects.filter(email=self.cleaned_data.get('email'))) > 0:
            self.add_error('email', "Этот email уже использован")
            ret = False
        if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
            self.add_error('password1', "Пароли не совпадают")
            self.add_error('password2', "Пароли не совпадают")
            ret = False
        return ret

    def saveUser(self):
        if self.is_valid_():
            user = CustomUser.objects.create_user(username=self.cleaned_data.get('login'),
                                                  email=self.cleaned_data.get('email'),
                                                  first_name=self.cleaned_data.get('nickName'),
                                                  password=self.cleaned_data.get('password1'),
                                                 )
            user.avatar = self.cleaned_data.get('avatar')
            user.save()
            return True
        return False

class AvatarSettingsForm(forms.Form):
    avatar = forms.ImageField()

class MainSettingsForm(forms.Form):
    login = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=30)
    nickName = forms.CharField(max_length=30)

    def is_valid_(self, user):
        ret = self.is_valid()
        try:
            u = CustomUser.objects.get(username=self.cleaned_data.get('login'))
            if u.user_ptr_id != user.user_ptr_id:
                self.add_error('login', "Это имя уже занято")
                ret = False
        except CustomUser.DoesNotExist:
            pass
        try:
            u = CustomUser.objects.get(email=self.cleaned_data.get('email'))
            if u.user_ptr_id != user.user_ptr_id:
                self.add_error('email', "Этот email уже использован")
                ret = False
        except CustomUser.DoesNotExist:
            pass

        return ret

class PswSettingsForm(forms.Form):
    password1 = forms.CharField(max_length=30)
    password2 = forms.CharField(max_length=30)

    def is_valid_(self):
        ret = self.is_valid()
        if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
            self.add_error('password1', "Пароли не совпадают")
            self.add_error('password2', "Пароли не совпадают")
            ret = False
        return ret

class AvatarSettingsForm(forms.Form):
    avatar = forms.ImageField()

class AnswerForm(forms.Form):
    content = forms.CharField()

class QuestionForm(forms.Form):
    title = forms.CharField(max_length=200)
    content = forms.CharField()
    tags = forms.CharField(max_length=62)
        