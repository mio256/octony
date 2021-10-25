from django.urls import path

from . import views

app_name = 'board'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('thread', views.ThreadView.as_view(), name='thread'),
    path('thread/favorite', views.RankFavoriteView.as_view(), name='rank_favorite'),
    path('thread/response', views.RankResponseView.as_view(), name='rank_response'),
    path('terms', views.TermsView.as_view(), name='terms'),
    path('explain', views.ExplainView.as_view(), name='explain'),
    path('<int:pk>/', views.ResponseView.as_view(), name='response'),
    path('<int:thread_id>/favorite/', views.add_favorite, name='favorite'),
    path('history', views.HistoryView.as_view(), name='history'),
]
