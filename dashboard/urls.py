from django.urls import path
from .views import dashboard, accounts_list,account_upgrade, account_detail

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('accounts/', accounts_list, name='accounts'),
    path('accounts/<int:id>/', account_detail, name='account_detail'),
    path('accounts/<int:id>/upgrade', account_upgrade, name='upgrade_to_counsellor'),
]
