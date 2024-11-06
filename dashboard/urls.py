from django.urls import path
from .views import (account_create, account_delete, account_detail, account_edit, account_upgrade, uchats, uchat_detail,
    accounts_list, alerts, dashboard, reports, send_feedback_view)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('accounts/', accounts_list, name='accounts'),
    path('alert/', alerts, name='alert'),
    path('reports/', reports, name='reports'),
    path('accounts/<int:id>/', account_detail, name='account_detail'),
    path('accounts/<int:id>/delete', account_delete, name='account_delete'),
    path('accounts/create', account_create, name='account_create'),
    path('accounts/<int:id>/edit', account_edit, name='account_edit'),
    path('accounts/<int:id>/upgrade', account_upgrade, name='upgrade_to_counsellor'),
    path('uchats/', uchats, name='uchats'),
    path('uchats/<int:id>/', uchat_detail, name='uchat_detail'),
    path('<str:chat_id>/send-feedback/', send_feedback_view, name='send_feedback'),
]
