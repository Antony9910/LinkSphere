from django.contrib import admin

# Register your models here.
from SocialApp.models import Posts,Stories,UserProfile

admin.site.register(Posts)
admin.site.register(Stories)
admin.site.register(UserProfile)