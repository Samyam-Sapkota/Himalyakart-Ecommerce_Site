from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Contact_Details



def _set_contact_id(request):
    contact_id = request.session.session_key
    if not contact_id:
        contact_id = request.session.create()
    return contact_id


# Create your views here.
def contact_views (request):
    if request.method == 'POST':
        users_name = request.POST.get('users_name') 
        users_contact_no = request.POST.get('users_contact_no') 
        users_email = request.POST.get('users_email') 
        users_message = request.POST.get('users_message') 
        
        create_new_message = Contact_Details.objects.all()
        create_new_message.create(
            users_name=users_name,
            users_contact_no =users_contact_no,
            users_email =users_email,
            users_message = users_message,
            contact_details_id=_set_contact_id(request)
        )
        messages.success(request, 'Your queries was successfully submitted')

        return redirect('home_view')
    return render(request,'others/contact.html')