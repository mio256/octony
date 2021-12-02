from django.contrib import admin
from django import forms

from .models import Response, Thread


class ResponseInline(admin.StackedInline):
    model = Response
    extra = 1


class ThreadAdmin(admin.ModelAdmin):
    list_filter = ['update_date']
    search_fields = ['title']
    list_display = ('title', 'update_date', 'responses', 'favorites')
    inlines = [ResponseInline]


admin.site.register(Thread, ThreadAdmin)
