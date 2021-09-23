from rest_framework import generics, permissions, status
from rest_framework.response import Response

from bank.models import AccountHistory
from bank.serializers import AccountHistoryDetailSerializer
from bank.services import TransferService, ChangeRateService, TopUpService
from bank.validators import TransferValidator, TopUpValidator
from users.permissions import IsOwner


class TransferAPIView(generics.GenericAPIView):
    service_class = TransferService
    validator_class = TransferValidator

    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def post(self, request, *args, **kwargs):

        account_id_card = request.POST.get('ID_card')
        transfer = request.POST.get('money')
        sender = request.user

        if self.validator_class.validator_is_correct(sender, transfer, account_id_card):
            self.service_class.transfer(sender, account_id_card, transfer)
            return Response('ok')
        else:
            return Response('you wrote the data incorrectly or you do not have enough amount')


class ChangeRateAPIView(generics.GenericAPIView):
    service_class = ChangeRateService

    def post(self, request, *args, **kwargs):
        self.service_class.change_rate(request.user, request.POST.get('title_rate'))
        return Response('it ok')


class AccountHistoryDetailAPIView(generics.ListAPIView):
    serializer_class = AccountHistoryDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        return AccountHistory.objects.filter(sender=self.request.user.account.bank_account)


class BalanceIncreaseAPIView(generics.GenericAPIView):
    validator_class = TopUpValidator
    service_class = TopUpService

    def post(self, request, *args, **kwargs):
        balance = request.data.get('balance')
        if not self.validator_class.validate_balance(balance):
            return Response('Pass balance to top up', status=status.HTTP_400_BAD_REQUEST)

        self.service_class.top_up(request.user, balance)

        return Response('Ok', status=status.HTTP_200_OK)
