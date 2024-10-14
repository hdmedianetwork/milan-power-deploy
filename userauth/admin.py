from django.contrib import admin
from userauth.models import User

# Allows us to add more fields to the user table

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role']

# Register your models here.
admin.site.register(User, UserAdmin)