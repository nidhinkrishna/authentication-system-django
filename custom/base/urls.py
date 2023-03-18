from django.contrib import admin
from django.urls import path,include
from . import views
from .views import SignUpView, ActivateAccount

urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.loginpage,name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'), 
    path('logout/',views.logoutfunc,name='logout')
]
