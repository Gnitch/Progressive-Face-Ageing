from django.urls import path
# from django.conf import settings
# from django.conf.urls.static import static

from app.views import home, missingPersonForm, familyForm, find

app_name='app'
urlpatterns = [
    path('', home, name='home'),
    path('find/', find, name='find'),
    path('family-form/', familyForm, name='familyForm'),
    path('missing-person-form/', missingPersonForm, name='missingPersonForm'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
