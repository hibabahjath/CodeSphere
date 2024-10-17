from django.shortcuts import render,redirect

from store.forms import SignUp

from django.views.generic import View

from django.contrib import messages

# Create your views here.

class SignUpView(View):

    template_name="register.html"

    form_class=SignUp

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            messages.success("Account Created Successfully")

            return redirect('signup')
        
        else:

            messages.error("Failed to Create Account")

            return render(request,self.template_name,{"form":form_instance})
