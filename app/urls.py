from django.urls import path

from app.views import home, missingPersonForm, familyForm

app_name='app'
urlpatterns = [
    path('', home, name=''),
    path('family-form/', familyForm, name='familyForm'),
    path('mssing-person-form/', missingPersonForm, name='missingPersonForm'),
]
