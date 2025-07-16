from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from django.utils import timezone

# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name="Profile")
    about=models.CharField(max_length=200,null=True)
    address=models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=200,null=True)
    profilePic=models.ImageField(upload_to="profilePics",null=True,blank=True)
    dob=models.DateField(null=True)
    bio=models.CharField(max_length=50,null=True)
    following=models.ManyToManyField("self",related_name="followed_by",symmetrical=False)
    block=models.ManyToManyField("self",related_name="block_user",symmetrical=False)
    
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
    post=models.ForeignKey(Posts,on_delete=models.CASCADE,related_name="postname")
    
    def __str__(self):
        return self.text
    
class Stories(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="userstories")
    text=models.CharField(max_length=200)
    post_image=models.ImageField(upload_to="stories",null=True,blank=True)
    created_date=models.DateField(auto_now_add=True)
    # exp=created_date+timezone.timedelta(days=1)
    expiry_date=models.DateField()
    def __str__(self):
        return self.text
    def save(self,*args,**kwargs):
        if not self.expiry_date:
            self.expiry_date=self.created_date+timezone.timedelta(days=1)
        super().save(*args,**kwargs)
#create signal for creating userprofile object
def create_profile(sender,created,instance,**kwargs): #created:whether objects are created or not
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_profile,sender=User)  #signal post_save ayi connection ahnu ithu eppolanu connect cheyyane when User model is created