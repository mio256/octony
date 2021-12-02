from django import forms
from .models import Thread, Response


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
