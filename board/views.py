from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Thread
from .forms import NameForm

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form})


class IndexView(generic.ListView):
    template_name = 'board/index.html'
    context_object_name = 'latest_thread_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Thread.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-latest_date')[:6]


class ListView(generic.ListView):
    template_name = 'board/list.html'
    context_object_name = 'thread_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Thread.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-latest_date')


class DetailView(generic.DetailView):
    model = Thread
    template_name = 'board/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Thread.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Thread
    template_name = 'board/results.html'


class TermsView(generic.ListView):
    model = Thread
    template_name = 'board/terms.html'


class ExplainView(generic.ListView):
    model = Thread
    template_name = 'board/explain.html'

class NameView(generic.ListView):
    model = Thread
    template_name = 'board/name.html'


def create_thread(request):
    try:
        thread = Thread(
            thread_text=request.POST['thread_str'],
            pub_date=timezone.now(),
            latest_date=timezone.now(),
            favorite_num=0,
        )
    except (KeyError):
        # Redisplay the thread voting form.
        return render(request, 'board/index.html', {
            'error_message': "Error",
        })
    else:
        thread.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('board:index'))


def tweet(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    try:
        tweet = thread.response_set.create(
            response_text=request.POST['tweet_str'],
            name_text=request.POST['name_str'],
            tweet_date=datetime.now()
        )
    except (KeyError):
        # Redisplay the thread voting form.
        return render(request, 'board/detail.html', {
            'thread': thread,
            'error_message': "You didn't have a tweet.",
        })
    else:
        if '$' in tweet.name_text:
            if 'miomio' in tweet.name_text.split('$')[-1]:
                tweet.adminset()
            elif 'aozora' in tweet.name_text.split('$')[-1]:
                tweet.moderatorset()
            else:
                tweet.hashset(tweet.name_text.split('$')[-1])
            tweet.name_text = tweet.name_text.split('$')[0]
        else:
            tweet.hash_text = 0
        tweet.save()
        thread.update_date()
        thread.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('board:results', args=(thread.id,)))


def add_favorite(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    try:
        thread.add_favorite()
    except (KeyError):
        # Redisplay the thread voting form.
        return render(request, 'board/detail.html', {
            'thread': thread,
            'error_message': "You didn't have a thread",
        })
    else:
        thread.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('board:results', args=(thread.id,)))
