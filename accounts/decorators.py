from django.http import HttpResponseRedirect
from functools import wraps

def redirect_if_auth(redirect_url):
    def inner_function(function):
        @wraps(function)
        def wrapper(*args,**kwargs):
            request = args[0]
            if request.user.is_authenticated :
                return HttpResponseRedirect(redirect_to=redirect_url)

            return function(*args,**kwargs)
        
        return wrapper

    return inner_function
    