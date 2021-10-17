from django.urls import path

from . import views

app_name = 'board'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('list', views.ListView.as_view(), name='list'),
    path('create', views.create_thread, name='create_thread'),
    path('terms', views.TermsView.as_view(), name='terms'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:thread_id>/favorite/', views.add_favorite, name='favorite'),
    path('<int:thread_id>/tweet/', views.tweet, name='tweet'),
]
