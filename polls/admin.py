from django.contrib import admin

# Register your models here.
from .models import PhoneNumber

admin.site.register(PhoneNumber)