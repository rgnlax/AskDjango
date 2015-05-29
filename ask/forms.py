# coding=utf-8
from django import forms
from django.contrib import auth
from models import CustomUser

class RegisterForm(forms.Form):
    login = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=30)
    nickName = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)
    passwordConfirmation = forms.CharField(max_length=30)
    avatar = forms.ImageField()

    def is_valid_(self):
        ret = self.is_valid()
        if len(CustomUser.objects.filter(username=self.cleaned_data.get('login'))) > 0:
            self.add_error('login', "Это имя уже занято")
            ret = False
        if len(CustomUser.objects.filter(email=self.cleaned_data.get('email'))) > 0:
            self.add_error('email', "Этот email уже используется")
            ret = False
        if self.cleaned_data.get('password') != self.cleaned_data.get('passwordConfirmation'):
            self.add_error('password', "Пароли не совпадают")
            self.add_error('passwordConfirmation', "Пароли не совпадают")
            ret = False
        return ret

    def saveUser(self):
        if self.is_valid_():
            user = CustomUser(  
                    avatar='/uploads/' + login + '.png',
                    password=make_password(password), 
                    last_login=datetime.now(),
                    is_superuser=False, 
                    username=login, 
                    first_name=nickName, 
                    last_name="", 
                    email=email, 
                    is_staff=False, 
                    is_active=True,
                    date_joined=datetime.now())
            user.save()
            return True
        return False