from django.db import models

# Create your models here.

class Contact_Details(models.Model):
    users_name = models.CharField(max_length=30)
    users_contact_no = models.IntegerField()
    users_email = models.EmailField()
    users_message = models.TextField(max_length=300)
    contact_details_id = models.CharField(max_length=100,blank=True)


    def __str__(self):
        return self.contact_details_id