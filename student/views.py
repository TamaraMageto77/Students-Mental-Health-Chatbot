from django.contrib.auth import logout
from django.shortcuts import render, redirect


def homepage_view(request):
    return render(request, 'homepage.html')

def logout_view(request):
    """
    Handles student logout.
    """
    logout(request)
    return redirect('login') 