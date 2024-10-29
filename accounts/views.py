from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from accounts.models import Account  # Custom user model with roles
from .forms import RegisterForm, LoginForm, CustomSetPasswordForm, UpdateProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView


def homepage(request):
    return render(request, 'index.html')

def signup_view(request):
    """
    Handles user registration.
    On GET request, it renders the registration template.
    On POST request, it validates the form data, creates a new user, and logs them in.
    """
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            login(request, user, backend='accounts.backends.MyUserBackend')
            return JsonResponse({'status': 'success', "next_url": next_url})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    return render(request, 'accounts/register.html', {"next_url": next_url})


def sigin_view(request):
    """
    Handles user login.
    Validates the form data and logs the user in if valid.
    """
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user, backend='accounts.backends.MyUserBackend')
                return JsonResponse({'status': 'success', "next_url": next_url})
            else:
                form.add_error(None, "Invalid email or password")
        return JsonResponse({'status': 'error', 'errors': form.errors})
    return render(request, 'accounts/login.html', {"next_url": next_url})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')


@login_required
def profile(request):
    """
    Handles profile viewing and updating.
    Allows users to view and edit their profile.
    """
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def users(request):
    """
    Displays a list of all users, excluding the currently logged-in user.
    """
    users_list = Account.objects.exclude(id=request.user.id)
    return render(request, 'accounts/users.html', {'users': users_list})


# User CRUD views
class UsersCreateView(LoginRequiredMixin, CreateView):
    model = Account
    fields = ['email', 'fullname', 'account_type', 'profile_image']  # Customize fields
    template_name = 'accounts/new_user.html'
    success_url = reverse_lazy('users')


class UsersUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    fields = ['email', 'fullname', 'account_type', 'profile_image']
    template_name = 'accounts/new_user.html'
    success_url = reverse_lazy('users')


class UsersDetailView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'accounts/user_detail.html'


class UsersDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = 'accounts/user_delete.html'
    success_url = reverse_lazy('users')


# Custom password reset views
class MyPasswordResetView(PasswordResetView):
    template_name = 'accounts/my_password_reset_form.html'
    email_template_name = 'accounts/my_password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if not Account.objects.filter(email=email).exists():
            messages.warning(self.request, 'No user found with this email')
            return self.form_invalid(form)
        return super().form_valid(form)


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/my_password_reset_done.html'


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/my_password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
    post_reset_login = True


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/my_password_reset_complete.html'
