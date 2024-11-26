from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def study_planner_view(request):
    return render(request, 'study_planner.html')