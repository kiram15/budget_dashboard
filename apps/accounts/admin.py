from django.contrib import admin
from .models import Institution, PlaidItem, Account

admin.site.register(Institution)
admin.site.register(PlaidItem)
admin.site.register(Account)