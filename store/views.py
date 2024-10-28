from django.shortcuts import render,redirect

from store.forms import SignUp,SignIn,UserProfileForm,ProjectForm

from django.urls import reverse_lazy

from django.contrib.auth import authenticate,login,logout

from django.views.generic import View,FormView,CreateView,TemplateView

from django.contrib import messages

from store.models import Project

# Create your views here.

# class SignUpView(View):

#     template_name="register.html"

#     form_class=SignUp

#     def get(self,request,*args,**kwargs):

#         form_instance=self.form_class()

#         return render(request,self.template_name,{"form":form_instance})
    
#     def post(self,request,*args,**kwargs):

#         form_instance=self.form_class(request.POST)

#         if form_instance.is_valid():

#             form_instance.save()

#             messages.success("Account Created Successfully")

#             return redirect('signin')
        
#         else:

#             messages.error("Failed to Create Account")

#             return render(request,self.template_name,{"form":form_instance})

class SignUpView(CreateView):

    template_name="register.html"

    form_class=SignUp

    success_url=reverse_lazy("signin")

class SignInView(FormView):

    template_name="login.html"

    form_class=SignIn

    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            uname=form_instance.cleaned_data.get("username")

            pwd=form_instance.cleaned_data.get("password")

            user_obj=authenticate(username=uname,password=pwd)

            if user_obj:

                login(request,user_obj)

                return redirect("index")
        
        return render(request,self.template_name,{"form":form_instance})

class IndexView(View):

    template_name="index.html"

    def get(self,request,*args,**kwargs):

        qs=Project.objects.all().exclude(developer=request.user)

        return render(request,self.template_name,{"data":qs})

class LogoutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")

# function based View
# def logout_view(request,*args,**kwargs):

#     logout(request)

#     return redirect("signin")

class UserProfileEditView(View):

    template_name="profile-edit.html"

    form_class=UserProfileForm

    def get(self,request,*args,**kwargs):

        profile_user_instance=request.user.profile

        form_instance=UserProfileForm(instance=profile_user_instance)

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        user_profile_instance=request.user.profile

        form_instance=self.form_class(request.POST,instance=user_profile_instance,files=request.FILES)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("index")
        
        return render(request,self.template_name,{"form":form_instance})
    
class ProjectCreateView(View):

    template_name="project_add.html"

    form_class=ProjectForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST,files=request.FILES)

        form_instance.instance.developer=request.user

        if form_instance.is_valid():

            form_instance.save()

            return redirect("index")
        
        return render(request,self.template_name,{"form":form_instance})

class MyProjectListView(View):

    template_name="my_projects.html"

    def get(self,request,*args,**kwargs):

        qs=Project.objects.filter(developer=request.user)

        return render(request,self.template_name,{"data":qs})
    
class ProjectUpdateView(View):

    template_name="project_update.html"

    form_class=ProjectForm

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        project_objects=Project.objects.get(id=id)

        form_instance=self.form_class(instance=project_objects)

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        project_objects=Project.objects.get(id=id)

        form_instance=self.form_class(request.POST,instance=project_objects,files=request.FILES)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("my-project")
        
        return render(request,self.template_name,{"form":form_instance})
    
class ProjectDetailView(View):

    template_name="project-detail.html"

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Project.objects.get(id=id)

        return render(request,self.template_name,{"data":qs})
    
    



