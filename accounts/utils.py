from django.conf import settings
from django.core.mail import send_mail
from threading import Thread

from django.db import models
import datetime
import pytz

# Get the timezone object for the timezone specified in settings.py
tz = pytz.timezone(settings.TIME_ZONE)

# Get the current time in the timezone
current_time = datetime.datetime.now(tz)


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
        