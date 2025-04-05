from django.shortcuts import render


def check_login_status(request):
    user_is_logged_in = False
    if request.user.is_authenticated:
        user_is_logged_in = True
    return {'user_is_logged_in':user_is_logged_in}