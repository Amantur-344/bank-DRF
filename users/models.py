from django.contrib.auth.models import User
from django.db import models

from bank.models import BankAccount


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='account')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE,
                                     related_name='bank_account')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name
