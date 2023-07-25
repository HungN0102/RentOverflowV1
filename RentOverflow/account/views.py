from django.shortcuts import render, redirect 
from .forms import CreateUserForm, LoginForm

# for login
from django.contrib.auth.models import auth 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            user.is_active = False 
            user.save()
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