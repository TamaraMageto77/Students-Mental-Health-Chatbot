from django.urls import path
from .views import homepage_view, logout_view

urlpatterns = [
    path('dashboard', homepage_view, name='student_dashboard'),
    path('logout/', logout_view, name='student_logout'),
]