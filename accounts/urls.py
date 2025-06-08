from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import PersonalRegistrationView, BusinessRegistrationView, UserProfileView

urlpatterns = [
    path('register/personal/', PersonalRegistrationView.as_view(), name='personal_register'),
    path('register/business/', BusinessRegistrationView.as_view(), name='business_register'),
    path('users/me/', UserProfileView.as_view(), name='user_profile'),
    path('login/', obtain_auth_token, name='login'), 
]