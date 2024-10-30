from django.urls import path
from .views import (
    homepage, about, signup_view, login_view, logout_view, profile, users,
    UsersCreateView, UsersDetailView, UsersUpdateView, UsersDeleteView,
    MyPasswordResetView, MyPasswordResetDoneView,
    MyPasswordResetConfirmView, MyPasswordResetCompleteView
)

urlpatterns = [
    path("", homepage, name="homepage"),
    path("about/", about, name="about"), 
    path("signup/", signup_view, name="signup"),# User registration
    path("login/", login_view, name="login"),# User login
    path("logout/", logout_view, name="logout"),# User logout
    path("profile/", profile, name="profile"),# User profile view/update
    # path("accounts/", users, name="accounts"),                  # List all users

    # User CRUD operations
    path("accounts/new/", UsersCreateView.as_view(), name="new_user"),         # Create new user
    path("accounts/<int:pk>/", UsersDetailView.as_view(), name="user_detail"), # User detail view
    path("accounts/<int:pk>/update/", UsersUpdateView.as_view(), name="user_update"), # Update user
    path("accounts/<int:pk>/delete/", UsersDeleteView.as_view(), name="user_delete"), # Delete user

    # Password reset views
    path("password_reset/", MyPasswordResetView.as_view(), name="password_reset"),                          # Password reset
    path("password_reset/done/", MyPasswordResetDoneView.as_view(), name="password_reset_done"),            # Password reset done
    path("reset/<uidb64>/<token>/", MyPasswordResetConfirmView.as_view(), name="password_reset_confirm"),   # Password reset confirm
    path("reset/done/", MyPasswordResetCompleteView.as_view(), name="password_reset_complete"),             # Password reset complete
]
