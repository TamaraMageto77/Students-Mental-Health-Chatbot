from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from accounts.models import Account
from django.shortcuts import redirect
from django.contrib import messages

def dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

def alerts(request):
    return render(request,  'admin/alerts.html')

def reports(request):
    return HttpResponse("Welcome to the Reports Dashboard!")


def uchats(request):
    return render(request,   'admin/uchat_sessions.html')

def uchat_detail(request):
    return render(request,   'admin/uchat.html')




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

@login_required
def account_delete(request, id):
    """
    Deletes a specific account and redirects to the accounts list.
    """
    try:
        account = Account.objects.get(id=id)
    except Account.DoesNotExist:
        return HttpResponse("Account not found.", status=404)
    
    if request.method == 'POST':
        account.delete()
        messages.success(request, 'Account deleted successfully.')
        return redirect('accounts')
    
    context = {'account': account}
    return render(request, 'admin/user_delete.html', context)

@login_required
def account_edit(request, id):
    """
    Displays and updates the details of a specific account.
    """
    try:
        account = Account.objects.get(id=id)
    except Account.DoesNotExist:
        return HttpResponse("Account not found.", status=404)
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        
        account.full_name = full_name
        account.email = email
        account.save()
        
        messages.success(request, 'Account updated successfully.')
        return redirect('account_detail', id=account.id)
    
    context = {'account': account}
    return render(request, 'admin/user_edit_form.html', context)

@login_required
def account_create(request):
    """
    Creates a new account.
    """
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(full_name, email, password)
        account = Account(full_name=full_name, email=email)
        account.set_password(password)
        account.save()
        
        messages.success(request, 'Account created successfully.')
        return redirect('account_detail', id=account.id)
    
    return render(request, 'admin/user_create_form.html')


@login_required
def account_upgrade(request, id):
    """
    Updates the details of a specific account.
    """
    try:
        account = Account.objects.get(id=id)
        account.account_type = 2
        account.is_counsellor = True
        account.save()
    except Account.DoesNotExist:
        return HttpResponse("Account not found.", status=404)
    
    context = {'account': account}
    return render(request, 'admin/account_detail.html', context)