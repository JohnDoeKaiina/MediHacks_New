from dotenv import load_dotenv
import os, requests
import qrcode
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST
from .forms import UserForm, HealthInfoForm,EmergencyContactForm, PrescritionForm
from .models import User, HealthInfo,EmergencyContact, Prescrition
from twilio.rest import Client
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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
    username=request.session.get('username')
    prescriptions = Prescrition.objects.filter(username=username)
    print("prescriptions",prescriptions)
    context={"username":username, 'MEDIA_URL': settings.MEDIA_URL,"prescriptions":prescriptions}
    return render(request, 'user/dashboard.html',context)


def landingpage(request):
    # Generate QR code
    username = request.session.get('username')
    print(f"{username} has accessed the landing page")
    Prescrition
    context = {
        'username':username,

    }
    return render(request, 'user/landingpage.html',context)


def create_qrcode(data,username):
            print(f"Creating a new QR for the data {data}")
            # Create a QR code instance
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L, 
                box_size=10, 
                border=4,  
            )
            qr.add_data(data)
            qr.make(fit=True)

            # Create an image from the QR code
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(f"./media/qrcodes/{username}.png")
            img.show()

def qrcode_landing_page(request, username):
    
    return render(request, 'user/qrcode_landing_page.html', {"username":username})

def qrcode_detail(request, username):
    user_profile = HealthInfo.objects.filter(username=request.session.get('username'))[0]
    emergency_contact = EmergencyContact.objects.filter(username=request.session.get('username'))[0]
    context = {'user_profile': user_profile, "emergency_contact":emergency_contact}
    return render(request, 'user/qrcode_details.html', context)

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
            create_qrcode(f'http://127.0.0.1:8000/qrcode/{username}',username)
            return redirect('emergency_contact')
    else:
        health_form = HealthInfoForm()
    
    return render(request, 'user/health_info_form.html', {'form': health_form})

def view_health_info(request):
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
            return redirect('dashboard')
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


def inform_emergency_contact(request, username):
    try:
        # Retrieve emergency contact info for the given username
        emergency_contact_info = EmergencyContact.objects.filter(username=request.session.get('username'))[0]
        phone_number = emergency_contact_info.phone_number
        # Retrieve Twilio credentials from settings
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        twilio_phone_number = settings.TWILIO_PHONE_NUMBER
        
        # Set up Twilio client
        client = Client(account_sid, auth_token)
        
        # Attempt to send the message
        message = client.messages.create(
            body='This is an emergency notification.',
            from_=twilio_phone_number,
            to=phone_number
        )
        
        # Return success response
        return JsonResponse({'message': 'SMS sent successfully!'})
    
    except EmergencyContact.DoesNotExist:
        # Handle case where no emergency contact is found for the username
        return JsonResponse({'error': 'Emergency contact not found.'}, status=404)
    
    except Exception as e:
        # Handle other exceptions (e.g., Twilio API errors)
        return JsonResponse({'error': str(e)}, status=500)

def seek_ai_help(request,username):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        
        if phone_number:
            # Set up Twilio client
            print("phone_numberphone_number",phone_number)
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            twilio_phone_number = settings.TWILIO_PHONE_NUMBER
            
            client = Client(account_sid, auth_token)
            
            try:
                print("Sending a message")
                # Compose your message
                message = client.messages.create(
                    body='This is an emergency notification.',
                    from_=twilio_phone_number,
                    to=phone_number
                )
                
                # Return a JSON response with success message
                return JsonResponse({'message': 'SMS sent successfully!'})
            
            except Exception as e:
                # Return error response if message sending fails
                return JsonResponse({'error': str(e)}, status=500)
        
        else:
            # Return error response if phone number is not provided
            return JsonResponse({'error': 'Phone number not provided.'}, status=400)
    
    # If GET request or initial rendering of the form
    return render(request, 'user/inform_emergency_contact.html')


def prescription_form(request):
    if request.method == 'POST':
        form = PrescritionForm(request.POST)
        if form.is_valid():
            form_info = form.save(commit=False)
            username = request.session.get('username')
            form_info.username = username
            form_info.patientid = 1
            form_info.save()
            return redirect('dashboard')
    else:
        form = PrescritionForm()
    
    return render(request, 'user/emergency_contact_form.html', {'form': form})