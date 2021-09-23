from django.db import models


class Currency(models.Model):
    title = models.CharField(max_length=3)  # short name exm: USD
    name = models.CharField(max_length=100)
    USD_rate = models.FloatField()

    def __str__(self):
        return self.title


class BankAccount(models.Model):
    ID_card = models.IntegerField()
    balance = models.FloatField(default=0)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE,
                                 related_name='account_currency')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.currency.title


class AccountHistory(models.Model):
    sender = models.ForeignKey(BankAccount, on_delete=models.CASCADE,
                               related_name='account_sender')
    recipient = models.ForeignKey(BankAccount, on_delete=models.CASCADE,
                                  related_name='account_recipient')
    date_created = models.DateTimeField(auto_now_add=True)
    money = models.CharField(max_length=20)

    def __str__(self):
        return self.money
