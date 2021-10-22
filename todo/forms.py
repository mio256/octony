from django import forms
from .models import User,Task

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['name']
        labels={
            'name':'名前',
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['title','content']
        labels={
            'title':'タスク名',
            'content':'内容',
        }