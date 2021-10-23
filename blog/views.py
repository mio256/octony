from django.views import generic


class IndexView(generic.TemplateView):
    template_name = 'blog/index.html'


class FirstView(generic.TemplateView):
    template_name = 'blog/first.html'
