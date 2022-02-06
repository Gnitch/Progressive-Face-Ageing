from django.urls import path

from app.views import home, missingPersonForm, familyForm, find

app_name='app'
urlpatterns = [
    path('', home, name='home'),
    path('find/', find, name='find'),
    path('family-form/', familyForm, name='familyForm'),
    path('missing-person-form/', missingPersonForm, name='missingPersonForm'),
]
