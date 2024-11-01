from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from accounts.models import Account, UserType  # Custom user model with roles
from .forms import RegisterForm, LoginForm, CustomSetPasswordForm, UpdateProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView


def homepage(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def chat(request):
    return render(request, 'chat_bot.html')


def signup_view(request):
    """
    Handles user registration.
    On GET request, it renders the registration template.
    On POST request, it validates the form data, creates a new user, and logs them in.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            login(request, user, backend='accounts.backends.AccountsBackend')
            if user.is_staff or user.is_counsellor:
                redirect_url = reverse_lazy('homepage')
            else:
                redirect_url = reverse_lazy
            return redirect(redirect_url)
    return render(request, 'register.html')


def login_view(request):
    """
    Handles user login.
    Validates the form data and logs the user in if valid.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user, backend='accounts.backends.AccountsBackend')
                return redirect("homepage")
            else:
                form.add_error(None, "Invalid email or password")
        return render(request, 'login.html', {"form":form})
    return render(request, 'login.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('homepage')


@login_required
def profile(request):
    """
    Handles profile viewing and updating.
    Allows users to view and edit their profile.
    """
    if request.method == 'POST':
        form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})


@login_required
def users(request):
    """
    Displays a list of all users, excluding the currently logged-in user.
    """
    users_list = Account.objects.exclude(id=request.user.id)
    return render(request, 'users.html', {'users': users_list})


# User CRUD views
class UsersCreateView(LoginRequiredMixin, CreateView):
    model = Account
    fields = ['email', 'fullname', 'account_type',
              'profile_image']  # Customize fields
    template_name = 'new_user.html'
    success_url = reverse_lazy('users')


class UsersUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    fields = ['email', 'fullname', 'account_type', 'profile_image']
    template_name = 'new_user.html'
    success_url = reverse_lazy('users')


class UsersDetailView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'user_detail.html'


class UsersDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = 'user_delete.html'
    success_url = reverse_lazy('users')


# Custom password reset views
class MyPasswordResetView(PasswordResetView):
    template_name = 'my_password_reset_form.html'
    email_template_name = 'my_password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if not Account.objects.filter(email=email).exists():
            messages.warning(self.request, 'No user found with this email')
            return self.form_invalid(form)
        return super().form_valid(form)


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'my_password_reset_done.html'


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'my_password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
    post_reset_login = True


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'my_password_reset_complete.html'
