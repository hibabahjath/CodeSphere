from django.shortcuts import render,redirect,get_object_or_404

from store.forms import SignUp,SignIn,UserProfileForm,ProjectForm,PasswordResetForm

from django.contrib import messages

from django.db.models import Sum

from django.contrib.auth.models import User

from django.urls import reverse_lazy

from django.contrib.auth import authenticate,login,logout

from django.views.generic import View,FormView,CreateView,TemplateView

from django.contrib import messages

from decouple import config

from store.models import Project,WishListItem,Order

from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator

from django.core.mail import send_mail

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

def send_email():

    send_mail(
    "codehub project download",
    "you have completed purchase of project",
    "bahjath107@gmail.com",
    ["sr4sarath18@gmail.com"],
    fail_silently=False,
)

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
    
class AddtoWishListView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        project_object=get_object_or_404(Project,id=id)

        try:

            request.user.basket.basket_item.create(project_object=project_object)

            messages.succes(request,"Added to WishList")
        
        except Exception as e:

            messages.error(request,"Already Added")

        return redirect("index")

class MyWishListView(View):

    template_name="my_wishlist.html"

    def get(self,request,*args,**kwargs):

        qs=request.user.basket.basket_item.filter(is_order_placed=False)

        total=qs.values("project_object").aggregate(total=Sum("project_object__price")).get("total")

        print("tottal",total)

        return render(request,self.template_name,{"data":qs,"total":total})
    
class WishListItemDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        WishListItem.objects.get(id=id).delete()

        return redirect("my-wishlist")

import razorpay

class CheckOutView(View):

    template_name="checkout.html"

    def get(self,request,*args,**kwargs):

        # razorpay authentication
        KEY_ID= config('KEY_ID')

        KEY_SECRET= config('KEY_SECRET')

        # authenticate
        client=razorpay.Client(auth=(KEY_ID,KEY_SECRET))

        # amount total
        amount=request.user.basket.basket_item.filter(is_order_placed=False).values("project_object").aggregate(total=Sum("project_object__price")).get("total")

        data = { "amount": amount*100, "currency": "INR", "receipt": "order_rcptid_codesphere" }

        payment = client.order.create(data=data)

        order_id=payment.get("id")

        order_object=Order.objects.create(order_id=order_id,customer=request.user)

        wishlist_items=request.user.basket.basket_item.filter(is_order_placed=False)

        for wi in wishlist_items:

            order_object.wishlist_item_objects.add(wi)

            wi.is_order_placed=True

            wi.save()

        return render(request,self.template_name,{"key_id":KEY_ID,"amount":amount,"order_id":order_id})

@method_decorator(csrf_exempt,name="dispatch")
class PaymentVerification(View):

    def post(self,request,*args,**kwargs):

        print(request.POST)

        KEY_ID= config('KEY_ID')

        KEY_SECRET= config('KEY_SECRET')

        client = razorpay.Client(auth=(KEY_ID,KEY_SECRET))

        print("rzp authenticated")

        try:

            client.utility.verify_payment_signature(request.POST)

            order_id=request.POST.get("razorpay_order_id")

            print(order_id,"printing","b4 update")

            Order.objects.filter(order_id=order_id).update(is_paid=True)

            print("after update")

            send_email(

            )
            
            print("success")
        
        except:


            print("failed")

        return redirect("orders")

class MyOrdersView(View):

    template_name="myorders.html"

    def get(self,request,*args,**kwargs):

        qs=Order.objects.filter(customer=request.user)

        return render(request,self.template_name,{"data":qs})
    
class PasswordResetView(View):

    template_name="password_reset.html"

    form_class=PasswordResetForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            username=form_instance.cleaned_data.get("username")

            email=form_instance.cleaned_data.get("email")

            password1=form_instance.cleaned_data.get("password1")

            password2=form_instance.cleaned_data.get("password2")

            print(username,email,password1,password2)

            try:

                assert password1==password2,"Password Mismatch"

                user_object=User.objects.get(username=username,email=email)

                user_object.set_password(password2)

                user_object.save()

                return redirect("signin")

            except Exception as e:

                messages.error(request,f"{e}")

        return render(request,self.template_name,{"form":form_instance})


    
    



