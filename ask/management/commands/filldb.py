from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password
from random import randint, randrange
from datetime import timedelta, datetime
from loremipsum import get_sentence, get_paragraph, get_sentences, get_paragraphs
import pytz, re
from ask.models import Question, Answer, Tag, Like, CustomUser

users_count   =   10000
questions_count = 100000
answers_count  =  1000000
tags_count    =   10000
votes_count   =   2000000

class Command(BaseCommand):
    help = 'Filling databese with data'

    def handle(self, *args, **options):
        start_time = datetime.now()

        for user_id in range(1, users_count + 1):
            user = CustomUser(
                avatar='http://lorempixel.com/10%s/10%s/cats' % (user_id % 10, user_id % 10),
				id=user_id,
				password=make_password("password"),
				last_login=self.random_date(),
				is_superuser=False,
				username="user%s" % (user_id),
				first_name="",
				last_name="",
				email="",
				is_staff=False,
				is_active=True,
				date_joined=datetime(2014, 1, 1, 1, 0, 0, 0, pytz.UTC)
            )
            self.stdout.write("User#%d" % user_id)
            user.save()

        for question_id in range(1, questions_count + 1):
            text=''
            for i in get_paragraphs(randint(1, 4)):
                text += i

            question = Question(
                id=question_id,
                title=get_sentence(),
                content=text,
                author_id=randint(1, users_count),
                created=self.random_date(),
                rating=0
            )
            for q_mark in range(1, 5):
                value = randint(0, 1)
                if l_value == 0:
                    l_value = -1
                like = Like(author_id=randint(1, users_count), value=l_value)
                like.save()
                question.likes.add(like)
                question.rating += like.value
                self.stdout.write("Like")

            self.stdout.write("Question#%d" % question_id)
            question.save()

        for answer_id in range(1, answers_count + 1):
            text=''
            for i in get_paragraphs(randint(1, 2)):
				text += i

            answer = Answer(
                id=answer_id,
				content=text,
				author_id=randint(1, users_count),
				created=self.random_date(),
				question_id=randint(1, questions_count),
				rating=0
            )

            for q_mark in range(1, 2):
                value = randint(0, 1)
                if l_value == 0:
                    l_value = -1
                like = Like(author_id=randint(1, users_count), value=l_value)
                like.save()
                answer.likes.add(like)
                answer.rating += like.value
                self.stdout.write("Like")

            self.stdout.write("Answer#%d" % answer_id)
            answer.save()

        words = open('ask/words', 'r')
        tag_id = 1
        for tag_id in range(1, tags_count + 1):
			tag = Tag(
					id=tag_id,
					title=words.readline()[:-1])

			tag.save()

        words.close()

        for question_id in range(1, questions_count + 1):
            question = Question.objects.get(pk=question_id)
            for i in range(1, 4):
                question.tags.add(Tag.objects.get(pk=randint(1, tags_count)))

        end_time = datetime.now()
        self.stdout.write('Database filled successfully' + str(end_time - start_time))

    def random_date(self):

		start = datetime(2014, 1, 1, 1, 0, 0, 0, pytz.UTC)
		end = datetime(2015, 1, 1, 1, 0, 0, 0, pytz.UTC)

		delta = end - start
		int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
		random_second = randrange(int_delta)
		return start + timedelta(seconds=random_second)
