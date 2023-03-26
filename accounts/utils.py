from django.conf import settings
from django.core.mail import send_mail
from threading import Thread

from django.db import models
import datetime
import pytz

from functools import wraps

from django.contrib import messages
import requests
import os



# Get the timezone object for the timezone specified in settings.py
tz = pytz.timezone(settings.TIME_ZONE)

# Get the current time in the timezone
current_time = datetime.datetime.now(tz)


import re
special_char_regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')



class SendEmail(Thread):
    '''
    Using threads to send mails
    '''
    
    sender = settings.EMAIL_HOST_USER
    
    def __init__(self, subject, message, *receiver):
        self.recipient_list = [emails for emails in receiver]
        self.subject = subject
        self.message = message
        Thread.__init__(self)
        
    def run(self):
        send_mail(self.subject, self.message, self.sender, self.recipient_list)
    
    

class BaseModel(models.Model):
    '''
    Creating a base model
    '''
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True



def check_str_special(string):
    if special_char_regex.search(string):
        return True
    else:
        return False


def check_recaptcha(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            request.recaptcha_is_valid = None
            if request.method == 'POST':
                recaptcha_response = request.POST.get('g-recaptcha-response')
                data = {
                    'secret': "6LcettkkAAAAAMASfSo37zyFPBLpaVUKaPj7t5eV",
                    'response': recaptcha_response
                }
                r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
                result = r.json()
                print(result)
                if result['success']:
                    request.recaptcha_is_valid = True
                else:
                    request.recaptcha_is_valid = False
                    messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return view_func(request, *args, **kwargs)
        except Exception as e:
            print(e)
    return _wrapped_view


