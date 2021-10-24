from django import forms
from .models import Thread, Response, Question, Answer


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title']
        labels = {
            'title': 'スレッド名',
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['name', 'content', 'image']
        labels = {
            'name': '名前',
            'content': '内容',
            'image': '画像',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, }),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content']
        labels = {
            'title': 'スレッド名',
            'content': '内容',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, }),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['name', 'content', 'image']
        labels = {
            'name': '名前',
            'content': '内容',
            'image': '画像',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, }),
        }
