from django.contrib import admin
from .models import Security, Holding, InvestmentTransaction, HoldingSnapshot, SecurityPriceHistory

admin.site.register(Security)
admin.site.register(Holding)
admin.site.register(InvestmentTransaction)
admin.site.register(HoldingSnapshot)
admin.site.register(SecurityPriceHistory)