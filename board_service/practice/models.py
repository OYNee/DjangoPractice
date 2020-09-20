from django.db import models

# Create your models here.
'''
게시판 만들기

게시물의 구성은 '제목'/'내용'/'작성시간'
'''

class Post(models.Model):
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=2048)
    date = models.DateTimeField(auto_created=True, auto_now=True)