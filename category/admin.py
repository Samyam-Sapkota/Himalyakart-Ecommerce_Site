from django.contrib import admin
from .models import Categories
# Register your models here.

class display_more(admin.ModelAdmin):
    list_display=('Cat_Name','Cat_Slug','Cat_Description','Date_Created','Date_Modified')
    prepopulated_fields = {'Cat_Slug':('Cat_Name',)}

admin.site.register(Categories,display_more)