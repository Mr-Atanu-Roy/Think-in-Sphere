from django.db import models
from accounts.utils import BaseModel
from accounts.models import User

# Create your models here.
class UserCourseHistory(BaseModel):
    '''This model will contain all the histoty of course and its topic explored by user'''
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.TextField()
    type = models.CharField(choices=(("subject", "subject"), ("topic", "topic")), default="subject", max_length=255)
        
    def __str__(self):
        return self.request
    
    class Meta:
        verbose_name_plural = "User Course Search History"
        ordering = ['created_at']