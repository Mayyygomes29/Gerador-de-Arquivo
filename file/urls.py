from django.urls import path

from .views import reading_file, error


urlpatterns = [
    path('upload/', reading_file, name='upload'),
    path('error/', error, name='error'),
]
