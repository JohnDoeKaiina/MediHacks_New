from dotenv import load_dotenv
import os, requests
import qrcode
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

from .forms import UserForm
from .models import User

from django.contrib.auth.decorators import login_required

def user_exist(username,password):
    user = User.objects.filter(username=username, password=password)
    if user:
        return True
    else:
        return False


def valid_username(credential):
    username = credential.cleaned_data.get("username")
    user = User.objects.filter(username=username)
    if user:
        return False
    else:
        return True


def login_page(request):


    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            if user_exist(request.POST.get('username', ''),request.POST.get('password', '')):
                    print(f"Valid user login in")
                    messages.add_message(request, messages.INFO, 'Logged in!')
                    return redirect('/')
    else:
         form = UserForm()

    sanction_msg=''
    context = {
        'form': form,
        'sanction_msg':sanction_msg
    }
    return render(request, 'user/login.html', context)



def register_page(request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid() and valid_username(form):
                form.save()
                return redirect('/login')
    else:
        form = UserForm()
    context = {
        'form': form,

    }
    return render(request, 'user/register.html', context)

def dashboard(request):
    pass

@login_required
def landingpage(request):
    # Generate QR code
    username=request.user
    print(f"{request.user} has accessed the landing page")

    context = {
        'username':username,

    }
    return render(request, 'user/landingpage.html',context)


def health_info(request):
    if request.method == 'POST':
        health_form = HealthInfoForm(request.POST)
        print("health_formhealth_form",health_form)
        if health_form.is_valid():
            health_info = health_form.save(commit=False)
            print("equest.user.is_authenticated", request.user.is_authenticated, request.user.id)
            if request.user.is_authenticated:
                health_info.user = request.user
                health_info.user_id = request.user.id
            else:
                anonymous_user = User.objects.get_or_create(username='anonymous')[0]
                health_info.user = anonymous_user
            health_info.save()
            return redirect('emergency_contact')
    else:
        health_form = HealthInfoForm()
    
    return render(request, 'user/health_info_form.html', {'form': health_form})

def view_health_info(request):
    # Assuming you are fetching the profile of the currently logged-in user
    user_profile = HealthInfo.objects.filter(user_id=request.user.id)
    print("user_profileuser_profile",user_profile)
    context = {
        'user': user_profile
    }
    return render(request, 'user/view_health_info_form.html', context)

def emergency_contact(request):
    pass