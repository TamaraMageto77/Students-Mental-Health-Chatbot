from django.urls import path

from .views import study_planner_view

urlpatterns = [
    path('', study_planner_view, name='study_planner'),
]