from django.urls import path

from accounts.views import signin, register

app_name='accounts'
urlpatterns = [
    path('login/', signin, name='login'),
    path('register/', register, name='register'),
]
