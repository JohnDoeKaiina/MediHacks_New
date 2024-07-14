from django.urls import path
from .views import login_page, register_page, landingpage, health_info, emergency_contact, dashboard

urlpatterns = [

    path('', landingpage, name='landingpage'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('healthinfo/', health_info, name='health_info'),
    path('emergencycontact/', emergency_contact, name='emergency_contact'),
    path('dashboard/', dashboard, name='dashboard'),

]
