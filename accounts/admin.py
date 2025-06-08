from django.contrib import admin
from .models import PersonalProfile, BusinessProfile, User


admin.site.register(User)
admin.site.register(PersonalProfile)
admin.site.register(BusinessProfile)
