import datetime
import re
import hashlib

from django.db import models
from django.utils import timezone
from django.contrib import admin


class Thread(models.Model):
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published')
    update_date = models.DateTimeField('date published')
    favorites = models.IntegerField()

    def __str__(self):
        return self.title

    @ admin.display(
        boolean=True,
        ordering='update_date',
    )
    def was_update_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(hours=12) <= self.update_date <= now

    def get_title(self):
        return self.title

    def get_pub_date(self):
        return (self.pub_date+datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')

    def get_update_date(self):
        return (self.update_date+datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')

    def get_favorites(self):
        return self.favorites

    def get_responses(self):
        return self.response_set.count()

    def add_favorite(self):
        self.favorites += 1
        self.update()

    def update(self):
        self.update_date = timezone.now()


class Response(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    date = models.DateTimeField('date published')
    ip = models.CharField(max_length=32)
    trip = models.CharField(max_length=32)
    image = models.ImageField(upload_to='images', blank=True, null=True)

    def __str__(self):
        return self.content

    def was_special(self):
        if self.trip in ['管理者', 'モデレーター']:
            return True
        else:
            return False

    def get_thread(self):
        return self.thread

    def get_content(self):
        ngwords = ['死', 'ホモ', 'ばか', 'おっぱい', '乳首', 'ハゲ', 'アホ', '体位', '正常位', '死', 'きちがい', '殺す',
                   '出っ歯', 'ぶす', '短足', '糞', 'ファック', '害児', '土人', 'ばばあ', 'じじい', '包茎', '童貞', 'チビ',
                   '低能', 'クズ', 'バカ']
        for word in ngwords:
            if word in self.content:
                return "---NG WORD---"
        return self.content

    def get_name(self):
        return self.name

    def get_date(self):
        return (self.date+datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')

    def get_ip(self):
        return self.ip

    def get_trip(self):
        return self.trip

    def get_urls(self):
        pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
        urls = re.findall(pattern, self.content)
        return urls

    def get_id(self):
        str = self.ip + self.date.strftime('%Y%m%d')
        return hashlib.sha256(str.encode()).hexdigest()[:8]
