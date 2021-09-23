import random

from django.contrib.auth.models import User
from django.db import transaction

from bank.models import BankAccount, Currency, AccountHistory
from users.models import Account

NUM_ID_CARD = 16  # number of id card


def get_random_id(x=NUM_ID_CARD):
    random_num = int('{0:0{x}d}'.format(random.randint(0, 10 ** x - 1), x=x))

    bank_account = BankAccount.objects.filter(ID_card=random_num).first()

    if bank_account is not None:
        get_random_id()
    else:
        return random_num


class BankAccountServices:

    @classmethod
    def create(cls):
        bank_account = BankAccount.objects.create(
            ID_card=get_random_id(),
            currency=Currency.objects.filter(title='USD').first()
        )
        return bank_account


class TransferService:

    @classmethod
    @transaction.atomic
    def transfer(cls, sender, recipient_id_card, transfer: float) -> None:
        sender = Account.objects.filter(user=sender).first()
        recipient = BankAccount.objects.filter(ID_card=recipient_id_card).first()

        with transaction.atomic():
            if sender.bank_account.balance > float(transfer):
                transfer = float(transfer)

                currency_sender = sender.bank_account.currency.USD_rate  # курс отправителя, его курс к доллару
                currency_recipient = recipient.currency.USD_rate    # курс получателя

                transfer_usd = transfer // currency_sender
                result_transfer = transfer_usd * currency_recipient

                AccountHistory.objects.create(
                    sender=BankAccount.objects.filter(id=sender.bank_account.id).first(),
                    recipient=recipient,
                    money=result_transfer
                )

                sender.bank_account.balance -= float(result_transfer)
                sender.bank_account.save()

                recipient.balance += float(result_transfer)
                recipient.save()


class TopUpService:

    @classmethod
    def top_up(cls, user: User, balance: float) -> None:
        account = Account.objects.filter(user=user).first()
        account.bank_account.balance += float(balance)
        account.bank_account.save()


class ChangeRateService:

    @classmethod
    def change_rate(cls, user: User, currency_title):
        account = Account.objects.filter(user=user).first()
        bank_account = account.bank_account
        currency = Currency.objects.filter(title=currency_title).first()

        account_balance = float(bank_account.balance)
        usd = account_balance // float(bank_account.currency.USD_rate)

        bank_account.balance = usd * float(currency.USD_rate)
        bank_account.currency = currency
        bank_account.save()
