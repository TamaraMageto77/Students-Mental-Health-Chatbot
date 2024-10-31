from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from accounts.models import Account

def dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

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

@login_required
def accounts_list(request):
    """
    Displays a list of all accounts.
    """
    context = {}
    context['accounts'] = Account.objects.all()
    context['admins'] = Account.objects.filter(account_type=1).count()
    context['counsellors'] = Account.objects.filter(account_type=2).count()
    context['students'] = Account.objects.filter(account_type=3).count()
    return render(request, 'admin/accounts_list.html', context)

@login_required
def account_detail(request, id):
    """
    Displays the details of a specific account.
    """
    try:
        account = Account.objects.get(id=id)
    except Account.DoesNotExist:
        return HttpResponse("Account not found.", status=404)
    
    context = {'account': account}
    return render(request, 'admin/account_detail.html', context)

def account_delete(request, id):
    """
    Displays the details of a specific account.
    """
    try:
        account = Account.objects.get(id=id)
    except Account.DoesNotExist:
        return HttpResponse("Account not found.", status=404)
    
    context = {'account': account}
    return render(request, 'admin/user_delete.html', context)

def account_edit(request, id):
    """
    Displays the details of a specific account.
    """
    try:
        account = Account.objects.get(id=id)
    except Account.DoesNotExist:
        return HttpResponse("Account not found.", status=404)
    
    context = {'account': account}
    return render(request, 'admin/user_edit.html', context)

@login_required
def account_upgrade(request, id):
    """
    Updates the details of a specific account.
    """
    try:
        account = Account.objects.get(id=id)
        account.account_type = 2
        account.save()
    except Account.DoesNotExist:
        return HttpResponse("Account not found.", status=404)
    
    context = {'account': account}
    return render(request, 'admin/account_detail.html', context)