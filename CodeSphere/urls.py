"""
URL configuration for CodeSphere project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignUpView.as_view(),name="signup"),
    path('',views.SignInView.as_view(),name="signin"),
    path('index/',views.IndexView.as_view(),name="index"),
    path('logout/',views.LogoutView.as_view(),name="logout"),
    path('profile/edit/',views.UserProfileEditView.as_view(),name="profile-edit"),
    path('project/add/',views.ProjectCreateView.as_view(),name="project-add"),
    path('myworks/all/',views.MyProjectListView.as_view(),name="my-project"),
    path('project/<int:pk>/update/',views.ProjectUpdateView.as_view(),name="project-update"),
    path('project/<int:pk>/detail/',views.ProjectDetailView.as_view(),name="project-detail"),
    path('project/<int:pk>/add-to-wishlist/',views.AddtoWishListView.as_view(),name="add-to-wishlist"),
    path('wishlist/all/',views.MyWishListView.as_view(),name="my-wishlist"),
    path('wishlist/<int:pk>/delete/',views.WishListItemDeleteView.as_view(),name="delete-item"),
    path('checkout',views.CheckOutView.as_view(),name="checkout"),
    path('payment/verify',views.PaymentVerification.as_view(),name="verify-payment"),
    path('order/all',views.MyOrdersView.as_view(),name="orders"),
    path('passwordreset/',views.PasswordResetView.as_view()),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
