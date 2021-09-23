from django.urls import path, include

from bank.views import TransferAPIView, ChangeRateAPIView, AccountHistoryDetailAPIView, BalanceIncreaseAPIView

urlpatterns = [
    path('transfer/', TransferAPIView.as_view()),
    path('change-currency/', ChangeRateAPIView.as_view()),
    path('account-history/', AccountHistoryDetailAPIView.as_view()),
    path('top-up-balance/', BalanceIncreaseAPIView.as_view()),
]