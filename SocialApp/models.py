from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name="Profile")
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    profilePic=models.ImageField(upload_to="profilePics",null=True,blank=True)
    dob=models.DateField()
    bio=models.CharField(max_length=50)
    block=models.ManyToManyField("self",related_name="block",symmetrical=False)
    
    def __str__(self):
        return self.user.username
class Posts(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="PostUsers")
    title=models.CharField(max_length=100)
    post_image=models.ImageField(upload_to="posters",null=True,blank=True)
    created_date=models.DateTimeField(auto_now_add=True)
    liked_by=models.ManyToManyField(User,related_name="post_like")
    
    #Print title of post
    def __str__(self):
        return self.title 
    
class Comments(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="comment")
    text=models.CharField(max_length=200)
    created_date=models.DateField(auto_now_add=True)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE,related_name="post_name")
    
    def __str__(self):
        return self.text
    
class Stories(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="userstories")
    text=models.CharField(max_length=200)
    post_image=models.ImageField(upload_to="stories",null=True,blank=True)
    created_date=models.DateField(auto_now_add=True)
    exp=created_date+timezone.timedelta(days=1)
    expiry_date=models.DateField(exp)
    def __str__(self):
        return self.text
    def save(self,*args,**kwargs):
        if not self.expiry_date:
            self.expiry_date=self.created_date+timezone.timedelta(days=1)
        super().save(*args,**kwargs)