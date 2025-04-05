from django.contrib import admin
from .models import Contact_Details
# Register your models here.

class admin_display_more(admin.ModelAdmin):
    list_display = ['users_name','users_contact_no','users_email','users_message']


admin.site.register(Contact_Details,admin_display_more)