from bank.models import BankAccount
from users.models import Account


class TransferValidator:

    @classmethod
    def validator_is_correct(cls, sender, transfer, account_id_card):
        sender = Account.objects.filter(user=sender).first()

        if sender is not None:
            if float(transfer) <= float(sender.bank_account.balance):
                recipient = BankAccount.objects.filter(ID_card=account_id_card).first()
                if recipient is not None:
                    return True
        return False


class TopUpValidator:

    @classmethod
    def validate_balance(cls, balance: float) -> bool:
        if not balance:
            return False

        try:
            float(balance)
        except ValueError:
            return False
        return True
