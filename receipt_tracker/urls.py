"""
URL configuration for receipt_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path
from receiptTracker import views

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from receiptTracker.views import ReceiptListView, ReceiptDetailView, ReceiptCreateView, ReceiptUpdateView


urlpatterns = [
    # login system
    path('', views.home_redirect, name='home-redirect'),
    path('admin/', admin.site.urls),
    path('register/', views.user_registration, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('confirm_logout/', views.confirm_logout_view, name='confirm_logout'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    # logic system
    path('receipts/', ReceiptListView.as_view(), name='receipt-list'),
    path('receipts/<int:pk>/', ReceiptDetailView.as_view(), name='receipt-detail'),
    path('receipts/new/', ReceiptCreateView.as_view(), name='receipt-new'),
    path('receipts/<int:pk>/edit/', ReceiptUpdateView.as_view(), name='receipt-edit'),

]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()