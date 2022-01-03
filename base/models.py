from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    
    def __str__(self):
        return self.name
class Room(models.Model):
    host =  models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    #null=True means that the field is optional
    #blank=True means that the field is allowed to be empty
    description = models.TextField(null=True, blank=True) 
    #participants = 
    updated = models.DateTimeField(auto_now=True) #auto_now=True means that the field is updated every time the object is saved
    created = models.DateTimeField(auto_now_add=True) #auto_now_add=True means that the field is updated only when the object is first created

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated','-created'] #without '-' the list will be sorted in ascending order = oldest first
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]