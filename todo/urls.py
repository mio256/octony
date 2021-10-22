from django.urls import path

from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>', views.TaskView.as_view(), name='task'),
    path('<int:pk>/<int:task_id>/done', views.done, name='done'),
    path('<int:pk>/kill', views.kill, name='kill'),
]