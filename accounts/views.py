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
            login(request)          
        else :            
            errors = form.errors.as_data()             
            errors = list(errors.values())
            errors = errors[0][0]
            context = {'error':list(errors)[0]}           
            return render(request,'accounts/register.html',context) 
        
    return render(request,'accounts/register.html')

@redirect_if_auth('/')
def login(request):
    if request.method == 'POST' :
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,username=email,password=password)
        if user is None:
            context = {'error':'Invalid Credentials'}           
            return render(request,'accounts/login.html',context)
        else :
            login(request,user)
            print('Logged in')
            HttpResponseRedirect('/')

    return render(request,'accounts/login.html')

def logout(request):
    logout(request)
    print('Logged out')
    return render(request,'accounts/base.html')