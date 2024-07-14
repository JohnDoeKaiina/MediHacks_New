from dotenv import load_dotenv
import os, requests
import qrcode
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

from .forms import UserForm, HealthInfoForm,EmergencyContactForm
from .models import User, HealthInfo,EmergencyContact

from django.contrib.auth.decorators import login_required

def user_exist(username,password):
    user = User.objects.filter(username=username, password=password)
    print("useruseruseruser",user)
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
            username = request.POST.get('username')
            password = request.POST.get('password')
            if user_exist(username, password):
                # Store username in session
                request.session['username'] = username
                return redirect('/')  
            else:
                messages.error(request, 'Invalid username or password!')
    else:
        form = UserForm()

    context = {
        'form': form,
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
        context={}
        return render(request, 'user/dashboard.html',context)


def landingpage(request):
    # Generate QR code
    username = request.session.get('username')
    print(f"{username} has accessed the landing page")

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
            username = request.session.get('username')
            health_info.username = username
            health_info.user_id = 1
            health_info.save()
            return redirect('emergency_contact')
    else:
        health_form = HealthInfoForm()
    
    return render(request, 'user/health_info_form.html', {'form': health_form})

def view_health_info(request):
    # Assuming you are fetching the profile of the currently logged-in user
    user_profile = HealthInfo.objects.filter(username=request.session.get('username'))[0]
    print("user_profileuser_profile",user_profile)
    context = {
        'user': user_profile
    }
    return render(request, 'user/view_health_info_form.html', context)

def emergency_contact(request):
    if request.method == 'POST':
        emergency_form = EmergencyContactForm(request.POST)
        if emergency_form.is_valid():
            emergency_contact_info = emergency_form.save(commit=False)
            username = request.session.get('username')
            emergency_contact_info.username = username
            emergency_contact_info.user_id = 1
            emergency_contact_info.save()
            return redirect('view_emergency_contact')
    else:
        emergency_form = EmergencyContactForm()
    
    return render(request, 'user/emergency_contact_form.html', {'form': emergency_form})

def view_emergency_contact(request):
    # Assuming you are fetching the emergency contact of the currently logged-in user
    emergency_contact_info = EmergencyContact.objects.filter(username=request.session.get('username'))[0]
    
    context = {
        'emergency_contact': emergency_contact_info
    }
    return render(request, 'user/view_emergency_contact.html', context)