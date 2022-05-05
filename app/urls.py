from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from app import views

app_name='app'
urlpatterns = [
    path('', views.home, name='home'),
    path('find/', views.find, name='find'),
    path('person-detail/<int:person_id>', views.personDetail, name='personDetail'),
    path('status-update/<int:person_id>', views.statusUpdate, name='statusUpdate'),
    path('cyclegan/<int:person_id>', views.cyclegan, name='cyclegan'),
    path('family-form/', views.familyForm, name='familyForm'),
    path('search-person/', views.searchPerson, name='searchPerson'),
    path('missing-person-form/<int:family_pk>', views.missingPersonForm, name='missingPersonForm'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
