from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'index.html')


def about_project(request):
    return render(request,'others/about_project.html')


def about_team(request):
    return render(request,'others/our_team.html')

@login_required 
def profile_views(request):
    return render(request,'others/profile.html')