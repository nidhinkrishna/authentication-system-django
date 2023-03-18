from django.contrib import admin
from django.urls import path,include
from . import views
from .views import SignUpView, ActivateAccount
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.loginpage,name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'), 
    path('logout/',views.logoutfunc,name='logout'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='reset_password.html'),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='reset_confirm.html'),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='reset_complete.html'),name='password_reset_complete'),
]
