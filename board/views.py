import hashlib

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Thread
from .forms import ThreadForm, ResponseForm


class IndexView(generic.ListView):
    model = Thread
    template_name = 'board/index.html'
    context_object_name = 'latest_thread_list'

    def post(self, request, *args, **kwargs):
        thread = Thread(
            title = request.POST['title'],
            pub_date = timezone.now(),
            update_date = timezone.now(),
            favorites = 0,
        )
        thread.save()

        return HttpResponseRedirect(reverse('board:index'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ThreadForm()
        return context

    def get_queryset(self):
        return Thread.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-update_date')[:9]


class ThreadView(generic.ListView):
    model = Thread
    template_name = 'board/thread.html'
    context_object_name = 'thread_list'

    def post(self, request, *args, **kwargs):
        thread = Thread(
            title = request.POST['title'],
            pub_date = timezone.now(),
            update_date = timezone.now(),
            favorites = 0,
        )
        thread.save()

        return HttpResponseRedirect(reverse('board:index'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ThreadForm()
        return context

    def get_queryset(self):
        return Thread.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-update_date')


class ResponseView(generic.DetailView):
    model = Thread
    template_name = 'board/response.html'
    context_object_name = 'thread'

    def post(self, request, *args, **kwargs):
        thread = get_object_or_404(Thread, id=self.kwargs.get('pk', ''))

        names = request.POST['name']
        request.session['name'] = names
        if '$' in names:
            name = names.split('$')[0]
            str = names.split('$')[-1]
            if 'miomio' in str:
                trip = '管理者'
            elif 'aozora' in str:
                trip = 'モデレーター'
            else:
                trip = hashlib.sha256(str.encode()).hexdigest()[:8]
        else:
            name = names
            trip = '0'

        response = thread.response_set.create(
            content = request.POST['content'],
            date = timezone.now(),
            name = name,
            ip = get_cookie(request),
            trip = trip
        )

        thread.update()
        thread.save()

        return HttpResponseRedirect(reverse('board:response', args=(thread.id,))+'#end')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.session.get('name'):
            initial_dict = dict(name=self.request.session.get('name'))
        else:
            initial_dict = dict(name='ななしちゃん')
        context['form'] = ResponseForm(initial=initial_dict)

        return context


class TermsView(generic.TemplateView):
    template_name = 'board/terms.html'


class ExplainView(generic.TemplateView):
    template_name = 'board/explain.html'


def get_cookie(request):
    # 'HTTP_X_FORWARDED_FOR'ヘッダを参照して転送経路のIPアドレスを取得する。
    forwarded_addresses = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_addresses:
        # 'HTTP_X_FORWARDED_FOR'ヘッダがある場合: 転送経路の先頭要素を取得する。
        client_addr = forwarded_addresses.split(',')[0]
    else:
        # 'HTTP_X_FORWARDED_FOR'ヘッダがない場合: 直接接続なので'REMOTE_ADDR'ヘッダを参照する。
        client_addr = request.META.get('REMOTE_ADDR')
    return client_addr

def add_favorite(request,thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    thread.add_favorite()
    thread.save()
    return HttpResponseRedirect(reverse('board:index',))