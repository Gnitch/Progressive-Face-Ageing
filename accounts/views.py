from django.shortcuts import render

def login(request):
    return render(request, 'accounts/login.html')
    
def register(request):
    return render(request, 'accounts/register.html')    

def person(request):
    return render(request, 'accounts/person.html') 