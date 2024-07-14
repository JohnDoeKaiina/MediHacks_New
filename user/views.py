from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm, HealthInfoForm, EmergencyContactForm
from .models import User
from django.contrib.auth.decorators import login_required


def user_exist(credential):
    username = credential.cleaned_data.get("username")
    password = credential.cleaned_data.get("password")
    user = User.objects.filter(username=username, password=password)
    return user.exists()

def valid_username(credential):
    username = credential.cleaned_data.get("username")
    user = User.objects.filter(username=username)
    return not user.exists()

def login_page(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            if user_exist(form):
                messages.add_message(request, messages.INFO, 'Logged in!')
                return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'user/login.html', context)

def register_page(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid() and valid_username(form):
            form.save()
            return redirect('/user/login')
    context = {
        'form': form
    }
    return render(request, 'user/register.html', context)

def landingpage(request):
    return render(request, 'user/landingpage.html')



def health_info(request):
    if request.method == 'POST':
        health_form = HealthInfoForm(request.POST)
        if health_form.is_valid():
            health_info = health_form.save(commit=False)
            if request.user.is_authenticated:
                health_info.user = request.user
            else:
                # Handle the case where the user is not authenticated
                # For example, create a new anonymous user for this purpose
                anonymous_user = User.objects.get_or_create(username='anonymous')[0]
                health_info.user = anonymous_user
            health_info.save()
            return redirect('emergency_contact')
    else:
        health_form = HealthInfoForm()
    
    return render(request, 'user/health_info_form.html', {'form': health_form})


def emergency_contact(request):
    if request.method == 'POST':
        contact_form = EmergencyContactForm(request.POST)
        if contact_form.is_valid():
            emergency_contact = contact_form.save(commit=False)
            if request.user.is_authenticated:
                emergency_contact.user = request.user
            else:
                # Handle the case where the user is not authenticated
                # For example, create a new anonymous user for this purpose
                anonymous_user = User.objects.get_or_create(username='anonymous')[0]
                emergency_contact.user = anonymous_user
            emergency_contact.save()
            return redirect('profile')  # Redirect to user profile page or wherever appropriate
    else:
        contact_form = EmergencyContactForm()
    
    return render(request, 'user/emergency_contact_form.html', {'form': contact_form})