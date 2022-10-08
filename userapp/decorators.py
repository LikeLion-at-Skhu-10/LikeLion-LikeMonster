from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages

def login_message_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return function(request, *args, **kwargs)
    return wrap