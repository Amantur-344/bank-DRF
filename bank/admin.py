from django.contrib import admin

from bank.models import Currency, BankAccount, AccountHistory

admin.site.register(Currency)
admin.site.register(BankAccount)
admin.site.register(AccountHistory)
