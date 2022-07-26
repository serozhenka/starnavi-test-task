from django.contrib import admin

from .models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'created', 'last_activity', 'is_staff')


admin.site.register(Account, AccountAdmin)

