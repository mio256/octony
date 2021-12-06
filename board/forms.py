from django import forms
from .models import Thread, Response
# myproject/forms.py

from django import forms
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse


class ContactForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "お名前",
        }),
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "メールアドレス",
        }),
    )
    message = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': "お問い合わせ内容",
        }),
    )

    def send_email(self):
        subject = "お問い合わせ"
        message = self.cleaned_data['message']
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        from_email = '{name} <{email}>'.format(name=name, email=email)
        recipient_list = [settings.EMAIL_HOST_USER]  # 受信者リスト
        try:
            send_mail(subject, message, from_email, recipient_list)
        except BadHeaderError:
            return HttpResponse("無効なヘッダが検出されました。")


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
