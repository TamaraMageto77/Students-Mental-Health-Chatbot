from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from accounts.models import Account

def homepage(request):
    return render(request, 'admin/admin_dashboard.html')
    
def accounts(request):
    return HttpResponse("Welcome to the Admin Accounts Dashboard!")

def alerts(request):
    return HttpResponse("Welcome to the Alerts Dashboard!")

def reports(request):
    return HttpResponse("Welcome to the Reports Dashboard!")


@login_required
def users(request):
    """
    Displays a list of all users, excluding the currently logged-in user.
    """
    users_list = Account.objects.exclude(id=request.user.id)
    return JsonResponse(users_list)