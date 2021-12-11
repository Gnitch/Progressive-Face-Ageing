from django.urls import path

from app.views import home

app_name='app'
urlpatterns = [
    path('', home, name=''),
]
