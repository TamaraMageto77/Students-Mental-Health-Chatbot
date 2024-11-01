from django.urls import path
from .views import dashboard, accounts_list,account_upgrade, account_detail, account_delete, account_edit, alerts, account_edit_user

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('accounts/', accounts_list, name='accounts'),
    path('alert/', alerts, name='alert'),
    path('accounts/<int:id>/', account_detail, name='account_detail'),
    path('accounts/<int:id>/delete', account_delete, name='account_delete'),
    path('accounts/<int:id>/edit', account_edit, name='account_edit'),
    path('accounts/<int:id>/uedit', account_edit_user, name='account_edit_user'),
    path('accounts/<int:id>/upgrade', account_upgrade, name='upgrade_to_counsellor'),
]
