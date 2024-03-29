import datetime
import re
import hashlib
import math
import csv
from janome.tokenizer import Tokenizer

from django.db import models
from django.utils import timezone
from django.contrib import admin


# ネガポジ辞書を読む
np_dic = {}
fp = open("/home/mio256/mysite/pn.csv", "rt", encoding="utf-8")
# fp = open("pn.csv", "rt", encoding="utf-8")
reader = csv.reader(fp, delimiter='\t')
for i, row in enumerate(reader):
    name = row[0]
    np_dic[name] = row[1]


class Thread(models.Model):
    title = models.CharField(max_length=32)
    pub_date = models.DateTimeField('date published')
    update_date = models.DateTimeField('date published')
    favorites = models.IntegerField()
    responses = models.IntegerField()

    def __str__(self):
        return self.title

    @admin.display(
        boolean=True,
        ordering='update_date',
    )
    def was_update_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(hours=12) <= self.update_date <= now

    def get_title(self):
        return self.title

    def get_pub_date(self):
        return (self.pub_date +
                datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')

    def get_update_date(self):
        return (self.update_date +
                datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')

    def get_favorites(self):
        return self.favorites

    def get_responses(self):
        self.responses = self.response_set.count()
        return self.responses

    def get_pn(self):
        # 小説を読み込む
        responses = self.response_set.all()
        text = ""
        for i in responses:
            text += i.content

        # 形態素解析
        tok = Tokenizer()

        # 数える
        res = {"p": 0, "n": 0, "e": 0}
        for t in tok.tokenize(text):
            bf = t.base_form  # 基本形
            # 辞書にあるか確認
            if bf in np_dic:
                r = np_dic[bf]
                if r in res:
                    res[r] += 1

        # 結果を表示
        cnt = res["p"] + res["n"] + 1
        return str(math.floor(res["p"] / cnt * 100)) + "%"

    def add_favorite(self):
        self.favorites += 1
        self.update()

    def update(self):
        self.update_date = timezone.now()


class Response(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    trip = models.CharField(max_length=32)
    ip = models.CharField(max_length=32)
    date = models.DateTimeField('date published')
    content = models.TextField(max_length=1024)
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
        ngwords = [
            '死', 'ホモ', 'ばか', 'おっぱい', '乳首', 'ハゲ', 'アホ', '体位', '正常位', '死',
            'きちがい', '殺す', '出っ歯', 'ぶす', '短足', '糞', 'ファック', '害児', '土人', 'ばばあ',
            'じじい', '包茎', '童貞', 'チビ', '低能', 'クズ', 'バカ'
        ]
        for word in ngwords:
            if word in self.content:
                return "---NG WORD---"
        return self.content

    def get_name(self):
        return self.name

    def get_date(self):
        return (self.date +
                datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')

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
