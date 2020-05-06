"""Budgetproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from budget.views import *

urlpatterns = [
    path('index',indexpage,name="index"),
    path('logout',Budgetlogout.as_view(),name="logout"),
    path('Reg/',CreateRegForm.as_view(),name="Register"),
    path('Reg/login/',CreateUserLogin.as_view(),name="login"),
    path('Reg/login/userhome',UserHome.as_view(),name="userhome"),
    path('entry/',CreateBudget.as_view(),name="entry"),
    path("budgetlist/",ListBudget.as_view(),name="budgetlist"),
    path('view/<int:pk>',BudgetView.as_view(),name='budget_view'),
    path('edit/<int:pk>',UpdateBudget.as_view(),name="budget_edit"),
    path('delete/<int:pk>',BudgetDelete.as_view(),name='budget_delete'),
    path("datewise",DatewiseReview.as_view(),name='datewise'),
    path("categorywise",CategorywiseReview.as_view(),name="categorywise")

]
