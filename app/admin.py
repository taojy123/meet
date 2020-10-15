from django.contrib import admin

from app.models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):

    list_display = ['id', 'token', 'name', 'days', 'created_at']

