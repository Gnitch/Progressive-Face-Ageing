from django.shortcuts import render,redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from accounts.forms import UserRegisterForm
from accounts.decorators import redirect_if_auth

@redirect_if_auth('/')
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid() == True:
            obj = form.save() 
            signin(request)          
        else :            
            errors = form.errors.as_data()             
            errors = list(errors.values())        
            err = ''
            for error in errors :
                err = str(list(error[0])[0]) + ' '
            context = {'error':err}           
            return render(request, 'accounts/register.html', context) 
        
    return render(request, 'accounts/register.html')

@redirect_if_auth('/')
def signin(request):
    if request.method == 'POST' :
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is None:
            context = {'error':'Invalid Credentials'}           
            return render(request, 'accounts/login.html', context)
        else :
            login(request, user)
            return render(request, 'app/home.html')

    return render(request, 'accounts/login.html')

def signout(request):
    logout(request)
    return render(request, 'accounts/login.html')
