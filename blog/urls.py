from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('001', views.Blog001View.as_view(), name='blog001'),
    path('002', views.Blog002View.as_view(), name='blog002'),
]
