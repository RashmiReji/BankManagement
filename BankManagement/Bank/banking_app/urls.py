from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Import `admin` correctly
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_account/', views.create_account, name='create_account'),
    path('deposit_withdraw/', views.deposit_withdraw, name='deposit_withdraw'),
    path('transaction_history/', views.transaction_history, name='transaction_history'),
]
