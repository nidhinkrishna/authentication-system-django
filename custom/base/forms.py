from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=['name','email','password1','password2']