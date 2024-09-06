from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, CreateAccountForm, DepositWithdrawForm
from .models import Account, Transaction

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout

def logout(request):
    auth_logout(request)
    return redirect('home')  # Redirect to the home page after logout

@login_required
def dashboard(request):
    try:
        account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        # Handle the case where the account does not exist
        return redirect('create_account')  # or any other appropriate action
    # Your existing logic here
    return render(request, 'dashboard.html', {'account': account})
@login_required
def create_account(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('dashboard')
    else:
        form = CreateAccountForm()
    return render(request, 'create_account.html', {'form': form})

@login_required
def deposit_withdraw(request):
    if request.method == 'POST':
        form = DepositWithdrawForm(request.POST)
        if form.is_valid():
            account = Account.objects.get(user=request.user)
            amount = form.cleaned_data['amount']
            transaction_type = 'Deposit' if 'deposit' in request.POST else 'Withdrawal'

            if transaction_type == 'Withdrawal' and amount > account.balance:
                form.add_error(None, 'Insufficient funds')
                return render(request, 'deposit_withdraw.html', {'form': form})

            if transaction_type == 'Deposit':
                account.balance += amount
            else:
                account.balance -= amount

            account.save()

            Transaction.objects.create(
                account=account,
                transaction_id=f'TR{Transaction.objects.count() + 1}',
                type=transaction_type,
                amount=amount
            )
            return redirect('dashboard')
    else:
        form = DepositWithdrawForm()
    return render(request, 'deposit_withdraw.html', {'form': form})

@login_required
def transaction_history(request):
    user = request.user
    account = Account.objects.get(user=user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'transaction_history.html', {'transactions': transactions})

def home(request):
    return render(request, 'home.html')
