from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Account(models.Model):
    ACCOUNT_TYPES = (
        ('Savings', 'Savings'),
        ('Current', 'Current'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.account_number} - {self.user.username}'


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=20, unique=True)
    date = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.transaction_id} - {self.type}'
