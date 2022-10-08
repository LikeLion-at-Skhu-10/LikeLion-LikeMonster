from django.contrib import admin
from userapp.models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id','username','user_image',]
    list_display_links = ['id', 'username']