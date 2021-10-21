from django.urls import path

from . import views

app_name = 'board'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('thread', views.ThreadView.as_view(), name='thread'),
    path('terms', views.TermsView.as_view(), name='terms'),
    path('explain', views.ExplainView.as_view(), name='explain'),
    path('<int:pk>/', views.ResponseView.as_view(), name='response'),
    path('<int:thread_id>/favorite/', views.add_favorite, name='favorite'),
]