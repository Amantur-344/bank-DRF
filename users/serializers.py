from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from bank.serializers import BankAccountDetailSerializer
from bank.services import BankAccountServices
from users.models import Account


class AccountRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = ('first_name',
                  'last_name',
                  'email',
                  'password',
                  'password2')

    def validate(self, attrs):
        user = User.objects.filter(username=attrs['email']).first()
        if user:
            raise ValidationError({'Error': 'Email already exists'})
        if attrs['password'] != attrs['password2']:
            raise ValidationError({'Error': 'Passwords did not match'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'],
            password=make_password(validated_data['password'])
        )

        account = Account.objects.create(
            user=user,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            bank_account=BankAccountServices.create()
        )

        return account


class AccountDetailSerializer(serializers.ModelSerializer):
    # bank_account = BankAccountDetailSerializer(many=True)

    class Meta:
        model = Account
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email',
                  'bank_account',
                  )
        depth = 2
