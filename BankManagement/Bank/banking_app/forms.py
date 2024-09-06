from django import forms
from django.contrib.auth.models import User
from .models import Account, Transaction
import random

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CreateAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_type']

    def save(self, commit=True):
        # Create an instance of the Account without saving to the database
        account = super().save(commit=False)

        # Generate a random account number (for example, a 10-digit number)
        account.account_number = random.randint(1000000000, 9999999999)

        # Save the account instance
        if commit:
            account.save()

        return account
class DepositWithdrawForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']
