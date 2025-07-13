from django.shortcuts import render,redirect
from django.urls import reverse

from django.views.generic import FormView,CreateView

from SocialApp.forms import RegistrationForm

#Rendering this form into html page
class SignUpView(CreateView):
    # def get(self,request,*args,**kwargs):
    #     form=RegistrationForm()
    #     return render(request,"register.html",{"form":form})
   template_name="register.html"
   form_class=RegistrationForm
   def get_success_url(self):
      return reverse("login")
  
#    def post(self,request,*args,**kwargs):
#        form=RegistrationForm(request.POST)
#        if form.is_valid:
#            form.save()
#            print("Account Created Successfully")
#            return redirect("login")
#        else:
#            return render(request,"register.html",{"form":form})
