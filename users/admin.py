from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User

# Register your models here.


class UserAdmin(BaseUserAdmin):
    list_display = ["email", "phone_number", "is_admin", "is_moderator"]
    list_filter = ["is_admin", "is_moderator"]
    search_fields = ["email", "phone_number"]
    ordering = ["email"]


admin.site.register(User, UserAdmin)
