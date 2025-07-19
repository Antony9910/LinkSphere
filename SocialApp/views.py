from django.shortcuts import render,redirect
from django.urls import reverse

from django.views.generic import FormView,CreateView,TemplateView,View,UpdateView,DetailView,ListView

from SocialApp.forms import RegistrationForm,LoginForm,UserProfileForm,PostForm,CommentForm
from django.contrib.auth import authenticate,login,logout
from SocialApp.models import UserProfile,Posts

#Rendering this form into html page
class SignUpView(CreateView):
    # def get(self,request,*args,**kwargs):
    #     form=RegistrationForm()
    #     return render(request,"register.html",{"form":form})
   template_name="register.html"
   form_class=RegistrationForm
   def get_success_url(self):
      print("register success")
      return reverse("signin")
  
#    def post(self,request,*args,**kwargs):
#        form=RegistrationForm(request.POST)
#        if form.is_valid:
#            form.save()
#            print("Account Created Successfully")
#            return redirect("login")
#        else:
#            return render(request,"register.html",{"form":form})
class SignInView(FormView):
    template_name="login.html"
    form_class=LoginForm
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                print("Login Successfully")
                return redirect("Index")
        print("Login Failed")
        return render(request,"login.html",{"form":form})
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm 
    context_object_name="data"
    model=Posts
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse("Index")
    # def get_queryset(self):
    #     return Posts.objects.filter(user=self.request.user)
    
    #TO add user filed we write this code
    # def post(self,request,*args,**kwargs):
    #     form=PostForm(request.POST,files=request.FILES)
    #     if form.is_valid():
    #         form.instance.user=request.user  #Adding value of user to form before saving else error null constraint occur
    #         print("Added Successfully")
    #         form.save()
    #         return redirect("Index")
    #     else:
    #         return render(request,"index.html",{"form":form})
    # def get_success_url(self):
    #     return reverse("Index")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")    
class ProfileUpdateView(UpdateView):
    template_name="ProfileEdit.html"
    form_class=UserProfileForm
    model=UserProfile
    def get_success_url(self):
        return reverse("Index")
class ProfileDetailView(DetailView):
    template_name="ProfileDetail.html"
    model=UserProfile
    context_object_name="data"
    
class ProfileListView(View):
    def get(self,request,*args,**kwargs):
        qs=UserProfile.objects.all().exclude(user=request.user) #exclude used to move the user who is actually logged in 
        return render(request,"profileList.html",{"data":qs})
    
class FollowView(View):
    def post(self,request,*args,**kwargs):
        # print(request.POST)
        id=kwargs.get("pk")
        profile_object=UserProfile.objects.get(id=id)
        action=request.POST.get("action")
        if action=="follow":
            request.user.Profile.following.add(profile_object)
        elif action=="unfollow":
            request.user.Profile.following.remove(profile_object)
        return redirect("Index")
class PostLikeView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post_object=Posts.objects.get(id=id)
        action=request.POST.get("action")
        if action=="like":
            post_object.liked_by.add(request.user)
        elif action=="dislike":
            post_object.liked_by.remove(request.user)
        return redirect("Index")
class CommentView(CreateView):
    template_name="index.html"
    form_class=CommentForm
    
    def get_success_url(self):
        return reverse("Index")
    def form_valid(self,form):
        id=self.kwargs.get("pk")
        post_objects=Posts.objects.get(id=id)
        form.instance.user=self.request.user
        form.instance.post=post_objects
        return super().form_valid(form)
    