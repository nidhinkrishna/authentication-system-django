from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from .forms import SignUpForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.http import HttpResponse
import django


from django.contrib.auth import authenticate,login,logout


from django.utils.http import urlsafe_base64_decode

from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str

from django.contrib.auth.views import PasswordResetCompleteView

@login_required(login_url='login')
def home(request):

    return render(request,'home.html')

# Sign Up View
def signup(request):
    form= SignUpForm

    

    if request.method=='POST':
      
        form = SignUpForm(request.POST)
        
       
        if form.is_valid():
           

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, ('Please Confirm your email to login.'))
            

            return redirect('login')
        else:
            messages.error(request,"The two password fields didn’t match.")
   
            

    return render(request, 'signup.html', {'form': form}) 


    
class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
           
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('login')
            
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            
        


def loginpage(request):


    if request.method=="POST":
        email=request.POST.get('email').lower()
        password=request.POST.get('password')

        
        
        user=authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)
            # messages.success(request,'login success')
            return redirect('/')
        messages.error(request,'Username or password is incorrect')
          
        
    return render(request,'login.html')


    
def logoutfunc(request):
    user=request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request,'logout success')

        return redirect('login')


