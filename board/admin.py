from django.contrib import admin

from .models import Response, Thread,Question,Answer


class ResponseInline(admin.TabularInline):
    model = Response
    extra = 3


class ThreadAdmin(admin.ModelAdmin):
    list_filter = ['update_date']
    search_fields = ['title']
    list_display = ('title', 'update_date', 'responses', 'favorites')
    inlines = [ResponseInline]

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    list_filter = ['update_date']
    search_fields = ['title']
    list_display = ('title', 'update_date')
    inlines = [AnswerInline]

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Question, QuestionAdmin)
