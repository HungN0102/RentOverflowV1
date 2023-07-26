from django.shortcuts import render, redirect 
from .forms import CreateUserForm, LoginForm

# import models
from django.contrib.auth.models import User

# for registration
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate

from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str    
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

# for login
from django.contrib.auth.models import auth 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# for logout
from django.contrib.auth import logout

# Create your views here.
def register(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            user.is_active = False 
            user.save()

            # Email verification setup
            current_site = get_current_site(request)
            
            subject = 'Account verification email'
            
            message = render_to_string('account/registration/email_verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),
            })

            send_mail(
                subject,
                message,
                "sudokaname070899@gmail.com",
                [user.email],
                fail_silently=False,
            )
            return redirect('email_verification_sent')
    context = {'form': form}
    
    return render(request, 'account/registration/register.html', context=context)

def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth.login(request, user)
                return redirect('home')
            
    context_dict = {
        'form': form 
    }
    
    return render(request, 'account/general/my_login.html',context=context_dict)

def email_verification(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True 
        user.save()
        return redirect('email_verification_success')
    else:
        return redirect('email_verification_failed')
    

def email_verification_sent(request):
    return render(request, 'account/registration/email_verification_sent.html', context={})


def email_verification_success(request):
    return render(request, 'account/registration/email_verification_success.html', context={})
 

def email_verification_failed(request):
    return render(request, 'account/registration/email_verification_failed.html', context={})

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect("home")


@login_required(login_url='my_login')
def delete_account(request):
    user = User.objects.get(id=request.user.id)
    
    if request.method == 'POST':
        user.delete()
        
        return redirect('home')
    
    return render(request, 'account/general/delete_account.html',context={
        
    })

@login_required(login_url='my_login')
def dashboard(request):
    return render(request, 'account/general/dashboard.html', {
        'username': request.user.username
    })