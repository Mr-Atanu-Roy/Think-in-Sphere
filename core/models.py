from django.db import models
from accounts.utils import BaseModel
from accounts.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid

from core.utils import random_name

# Create your models here.

class ChatRoom(BaseModel):
    '''This model contains chatrooms created by user'''
    
    room_id = models.UUIDField(default=uuid.uuid4)
    room_name = models.CharField(max_length=300, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.room_name)
    
    class Meta:
        verbose_name_plural = "Chat Rooms"
        ordering = ['created_at']
    
    
class UserRequestHistory(BaseModel):
    '''This models contains all the search history of a user'''
    
    chatroom = models.ManyToManyField(ChatRoom)
    request = models.TextField()
    response = models.TextField(default="generated course")

    def __str__(self):
        return self.request
    
    class Meta:
        verbose_name_plural = "User Search History"
        ordering = ['created_at']
        
        
#SIGNALS
@receiver(post_save, sender=ChatRoom)
def chatroom_created_handler(sender, instance, created, *args, **kwargs):
    '''
    this signal is used to set a random name of chatroom if its left empty
    '''
                
    if created and instance.room_name is None: 
        instance.room_name = random_name()
        instance.save()
        
       