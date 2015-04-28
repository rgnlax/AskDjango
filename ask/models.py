from django.db import models
from django.contrib.auth.models import User, UserManager

class CustomUser(User):
    avatar = models.ImageField()
    objects = UserManager()

class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True)

class Like(models.Model):
    value = models.IntegerField()
    author = models.ForeignKey(CustomUser)

class Question(models.Model):
    title = models.TextField()
    content = models.TextField()
    created = models.DateTimeField()
    author = models.ForeignKey(CustomUser)
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField(default=0)
    likes = models.ManyToManyField(Like)

class Answer(models.Model):
    created = models.DateTimeField()
    question = models.ForeignKey(Question, null=True)
    content = models.TextField()
    author = models.ForeignKey(CustomUser)
    rating = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)
    likes = models.ManyToManyField(Like)
