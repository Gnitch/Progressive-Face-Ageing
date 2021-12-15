from django.urls import path

from accounts.views import login, register, person

app_name='accounts'
urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('person/', person, name='person'),
]
