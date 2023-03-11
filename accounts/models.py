from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import Usermanager

from .utils import *

import random

from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

otp_purpose_choices = (
    ("email_verification", "Email Verification"),
    ("reset_password", "Reset Password")
)


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    last_logout = models.DateTimeField(null=True, blank=True)
    
    objects = Usermanager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'auth_user'
        verbose_name_plural = "Think-In-Sphere User"
        ordering = ['date_joined']
    
    def __str__(self):
        return self.email
    

class UserProfile(BaseModel):
    '''
    User Profile models which has 1-1foreign key with user model. It stores all other necessary informations about User
    '''
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User")
    country = models.CharField(max_length=255, blank=True, null=True, default="", verbose_name="Country")
    city = models.CharField(max_length=255, blank=True, null=True, verbose_name="City")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date Of Birth")
    course_name = models.CharField(max_length=255, blank=True, null=True, default="", verbose_name="Current Persuing Course")
    institute_name = models.CharField(max_length=255, blank=True, null=True, default="", verbose_name="Current Institute")
    bot_prompt = models.TextField(verbose_name="User's Chatbot Prompt", default="The following is a conversation of a student with an AI assistant. The assistant is helpful, creative, clever, and very friendly and answers all the questions of the student very clearly.")
    
    class Meta:
        verbose_name_plural = "User Profile"
        ordering = ['created_at']
    
    def __str__(self):
        return str(self.user.email)
      
      
class OTP(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=255, null=True, blank=True)
    is_expired = models.BooleanField(default=False)
    purpose = models.CharField(choices=otp_purpose_choices, max_length=255, default="email_verification")
    
    class Meta:
        verbose_name_plural = "Auth OTP"
        ordering = ['created_at']
    
    def __str__(self):
        return self.otp

#SIGNALS
@receiver(post_save, sender=User)
def User_created_handler(sender, instance, created, *args, **kwargs):
    '''
    This User which will send a greetings email and create a UserProfile and OTP instance each time after a new user register, i.e., a NetflixUser is created
    '''
    if created:                
        subject = "Greetings From ThinkInSphere"
        message = f"Thank you for signing up with ThinkInSphere {instance.first_name}.... You have signed up using email - {instance.email}, at {instance.date_joined}"
        
        #starting the thread to send email
        SendEmail(subject, message, instance.email).start()
        
        #creating a UserProfile instance
        newProfile = UserProfile.objects.create(user=instance)
        newProfile.save()
        
        #creating a OTP instance
        newOTP = OTP.objects.create(user=instance)
        newOTP.save()
        

@receiver(post_save, sender=OTP)
def OTP_handler(sender, instance, created, *args, **kwargs):
    '''
    This signal send email based on purpose of OTP after an otp instance has been created
    '''
    if created :
        
        if instance.otp is None:
            instance.otp = random.randint(100000, 999999)   #setting a random otp if otp field is none
            instance.save()
        
        if instance.purpose.lower() == "email_verification":
            subject = "Verify Your Email"
            message = f"Your OTP for verifying email - {instance.user} is : {instance.otp}. This OTP is valid for the next 10 mintutes only"
            
        elif instance.purpose.lower() == "reset_password":
            subject = "Reset Your Password"
            message = f"Your OTP for reseting password for email - {instance.user} is : {instance.otp}. This OTP is valid for the next 10 mintutes only"

    
        #starting the thread to send email
        SendEmail(subject, message, instance.user.email).start()
    
    
      