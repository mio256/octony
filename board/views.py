import hashlib

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Response, Thread
from .forms import ThreadForm, ResponseForm

# myproject/views.py

from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import ContactForm


class ContactFormView(FormView):
    template_name = 'board/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_result')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class ContactResultView(TemplateView):
    template_name = 'board/contact_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success'] = "お問い合わせは正常に送信されました。"
        return context


class IndexView(generic.ListView):
    model = Thread
    template_name = 'board/index.html'
    context_object_name = 'latest_thread_list'

    def post(self, request, *args, **kwargs):
        thread = Thread(
            title=request.POST['title'],
            pub_date=timezone.now(),
            update_date=timezone.now(),
            favorites=0,
            responses=0,
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
        ).order_by('-update_date')[:27]


class ThreadView(generic.ListView):
    model = Thread
    template_name = 'board/thread.html'
    context_object_name = 'thread_list'

    def post(self, request, *args, **kwargs):
        thread = Thread(
            title=request.POST['title'],
            pub_date=timezone.now(),
            update_date=timezone.now(),
            favorites=0,
            responses=0,
        )
        thread.save()

        return HttpResponseRedirect(reverse('board:index'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ThreadForm()
        return context

    def get_queryset(self):
        list = Thread.objects.order_by('-update_date')
        return list


class RankFavoriteView(generic.ListView):
    model = Thread
    template_name = 'board/rank_favorite.html'
    context_object_name = 'thread_list'

    def post(self, request, *args, **kwargs):
        thread = Thread(
            title=request.POST['title'],
            pub_date=timezone.now(),
            update_date=timezone.now(),
            favorites=0,
            responses=0,
        )
        thread.save()

        return HttpResponseRedirect(reverse('board:index'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ThreadForm()
        return context

    def get_queryset(self):
        list = Thread.objects.order_by('-favorites')
        return list


class RankResponseView(generic.ListView):
    model = Thread, Response
    template_name = 'board/rank_response.html'
    context_object_name = 'thread_list'

    def post(self, request, *args, **kwargs):
        thread = Thread(
            title=request.POST['title'],
            pub_date=timezone.now(),
            update_date=timezone.now(),
            favorites=0,
            responses=0,
        )
        thread.save()

        return HttpResponseRedirect(reverse('board:index'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ThreadForm()
        return context

    def get_queryset(self):
        list = Thread.objects.all()
        for thread in list:
            thread.get_responses()
            thread.save()
        list = Thread.objects.order_by('-responses')
        return list


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
            content=request.POST['content'],
            date=timezone.now(),
            name=name,
            ip=get_ip(request),
            trip=trip
        )
        try:
            response.image = request.FILES['image']
        except KeyError:
            pass
        response.save()

        thread.update()
        thread.save()

        return HttpResponseRedirect(reverse('board:response', args=(thread.id,))+'#bottom')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.session.get('name'):
            initial_dict = dict(name=self.request.session.get('name'))
        else:
            initial_dict = dict(name='ななしちゃん')
        context['form'] = ResponseForm(initial=initial_dict)

        context['thread_id'] = self.kwargs['pk']

        return context


class TermsView(generic.TemplateView):
    template_name = 'board/terms.html'


class ExplainView(generic.TemplateView):
    template_name = 'board/explain.html'


def get_ip(request):
    # 'HTTP_X_FORWARDED_FOR'ヘッダを参照して転送経路のIPアドレスを取得する。
    forwarded_addresses = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_addresses:
        # 'HTTP_X_FORWARDED_FOR'ヘッダがある場合: 転送経路の先頭要素を取得する。
        client_addr = forwarded_addresses.split(',')[0]
    else:
        # 'HTTP_X_FORWARDED_FOR'ヘッダがない場合: 直接接続なので'REMOTE_ADDR'ヘッダを参照する。
        client_addr = request.META.get('REMOTE_ADDR')
    return client_addr


class HistoryView(generic.ListView):
    model = Thread
    template_name = 'board/history.html'
    context_object_name = 'thread_list'

    def get_queryset(self):
        list = []
        for pk in str(get_history(self.request)).split('-'):
            if pk != 'None':
                list.append(int(pk))
        history = [Thread.objects.get(id=i) for i in list]
        return history


def get_history(request):
    return request.session.get('history')


def add_favorite(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    thread.add_favorite()
    thread.save()
    try:
        history = request.session.get('history')
        request.session['history'] = str(history) + '-'+str(thread_id)
    except KeyError:
        request.session['history'] = str(thread_id)
    return HttpResponseRedirect(reverse('board:response', args=(thread.id,))+'#bottom')
