from django.contrib import admin

from .models import Response, Thread


class ResponseInline(admin.TabularInline):
    model = Response
    extra = 3


class ThreadAdmin(admin.ModelAdmin):
    list_filter = ['latest_date']
    search_fields = ['thread_text']
    list_display = ('thread_text', 'latest_date', 'was_published_recently')
    fieldsets = [
        (None,               {'fields': ['thread_text']}),
        ('pub_date', {'fields': [
         'pub_date'], 'classes': ['collapse']}),
        ('latest_data', {'fields': [
         'latest_date'], 'classes': ['collapse']}),
    ]
    inlines = [ResponseInline]


admin.site.register(Thread, ThreadAdmin)
