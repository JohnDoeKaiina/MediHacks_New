from django import forms
from .models import User,  HealthInfo, EmergencyContact, Prescrition


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
        }


class HealthInfoForm(forms.ModelForm):
    class Meta:
        model = HealthInfo
        fields = ['age', 'weight', 'height', 'blood_type', 'allergies','ongoing_medicines', 'medical_conditions']

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'relationship', 'phone_number']

class PrescritionForm(forms.ModelForm):
    class Meta:
        model = Prescrition
        fields = ('medicinename', 'quantity', 'days', 'time', 'status')