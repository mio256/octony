from django.views import generic


class IndexView(generic.TemplateView):
    template_name = 'blog/index.html'


class Blog001View(generic.TemplateView):
    template_name = 'blog/blog001.html'
