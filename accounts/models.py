from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('personal', 'Personal'),
        ('business', 'Business'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username
    

class PersonalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personal_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    professional_title = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BusinessProfile(models.Model):
    INDUSTRY_CHOICES = (
        ('technology', 'Technology'),
        ('healthcare', 'Healthcare'),
        ('finance', 'Finance'),
        ('retail', 'Retail'),
        ('manufacturing', 'Manufacturing'),
        ('other', 'Other'),
    )
    BUSINESS_SIZE_CHOICES = (
        ('small', 'Small (0-100 employees)'),
        ('medium', 'Medium (100-500 employees)'),
        ('big', 'Big (500+ employees)'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business_profile')
    business_name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=100, unique=True)
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    business_size = models.CharField(max_length=20, choices=BUSINESS_SIZE_CHOICES)

    def __str__(self):
        return self.business_name

#Done
