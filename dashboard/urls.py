from django.urls import path
from .views import (account_create, account_delete, account_detail, account_edit, account_upgrade,
    accounts_list, alerts, dashboard)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('accounts/', accounts_list, name='accounts'),
    path('alert/', alerts, name='alert'),
    path('accounts/<int:id>/', account_detail, name='account_detail'),
    path('accounts/<int:id>/delete', account_delete, name='account_delete'),
    path('accounts/create', account_create, name='account_create'),
    path('accounts/<int:id>/edit', account_edit, name='account_edit'),
    path('accounts/<int:id>/upgrade', account_upgrade, name='upgrade_to_counsellor'),
]
