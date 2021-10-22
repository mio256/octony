import hashlib
from django import forms

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import User, Task
from .forms import UserForm, TaskForm


class IndexView(generic.ListView):
    model = User
    template_name = 'todo/index.html'
    context_object_name = 'user_list'

    def post(self, request, *args, **kwargs):
        user = User(
            name=request.POST['name'],
        )
        user.save()

        return HttpResponseRedirect(reverse('todo:index'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserForm()
        return context


class TaskView(generic.DetailView):
    model = User
    template_name = 'todo/task.html'

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=self.kwargs.get('pk', ''))
        task = user.task_set.create(
            title=request.POST['title'],
            content=request.POST['content'],
        )
        task.save()
        return HttpResponseRedirect(reverse('todo:task', args=(user.id,)))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskForm()
        return context

def done(request,pk,task_id):
    user = get_object_or_404(User, id=pk)
    user.task_set.filter(id=task_id).delete()
    return HttpResponseRedirect(reverse('todo:task', args=(user.id,)))

def kill(request,pk):
    user = get_object_or_404(User, id=pk)
    user.delete()
    return HttpResponseRedirect(reverse('todo:index'))