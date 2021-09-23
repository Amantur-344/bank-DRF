from rest_framework import serializers

from bank.models import BankAccount, AccountHistory


class BankAccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ('id',
                  'ID_card',
                  'balance',
                  'currency.title'
                  )


class AccountHistoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountHistory
        fields = ('id',
                  'sender',
                  'recipient',
                  'date_created',
                  'money')
        depth = 2
