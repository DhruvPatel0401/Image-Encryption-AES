from django.urls import path
from . import views

urlpatterns = [
    path('encrypt/', views.encrypt_image, name='encrypt'),
    path('decrypt/', views.decrypt_image, name='decrypt'),
]