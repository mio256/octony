import datetime
import re
import hashlib

from django.db import models
from django.utils import timezone
from django.contrib import admin


class Thread(models.Model):
    thread_text = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published')
    latest_date = models.DateTimeField('date published')
    favorite_num = models.IntegerField()

    def __str__(self):
        return self.thread_text

    def print_pub_date(self):
        return (self.pub_date+datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')

    def update_date(self):
        self.latest_date = timezone.now()

    def print_latest_date(self):
        return (self.latest_date+datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')

    def print_count_response(self):
        return self.response_set.count()

    def print_title(self):
        return self.thread_text

    def add_favorite(self):
        self.favorite_num += 1
        self.update_date()

    @ admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def was_update_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(hours=12) <= self.latest_date <= now


class Response(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    response_text = models.CharField(max_length=255)
    name_text = models.CharField(max_length=255)
    hash_text = models.CharField(max_length=255)
    tweet_date = models.DateTimeField('date published')

    def __str__(self):
        return self.response_text

    def print_tweet_date(self):
        return (self.tweet_date+datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')

    def print_response_text(self):
        row = ['死', 'ホモ', 'ばか', 'おっぱい', '乳首', 'ハゲ', 'アホ', '体位', '正常位', '死', 'きちがい', '殺す',
               '出っ歯', 'ぶす', '短足', '糞', 'ファック', '害児', '土人', 'ばばあ', 'じじい', '包茎', '童貞', 'チビ',
                '低能', 'クズ','バカ']
        for word in row:
            if word in self.response_text:
                return "NG WORD"
        return self.response_text

    def print_urls(self):
        pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
        urls = re.findall(pattern, self.response_text)    
        return urls

    def was_special(self):
        if self.hash_text in ['管理者','モデレーター']:
            return True
        else:
            return False

    def hashset(self, str):
        self.hash_text = hashlib.sha256(str.encode()).hexdigest()[:8]

    def adminset(self):
        self.hash_text = "管理者"

    def moderatorset(self):
        self.hash_text = "モデレーター"
