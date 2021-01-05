from django.contrib import admin
from .models import Job
from django_admin_relation_links import AdminChangeLinksMixin
from django.utils.html import format_html
# Register your models here.


@admin.register(Job)
class JobAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    list_display = ('title', 'company', 'date', 'show_job_link')

    def show_job_link(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.link)

    show_job_link.short_description = "Job URL"

