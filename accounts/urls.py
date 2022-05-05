from django.urls import path

from accounts.views import signin, register, signout

app_name='accounts'
urlpatterns = [
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('register/', register, name='register'),
]
