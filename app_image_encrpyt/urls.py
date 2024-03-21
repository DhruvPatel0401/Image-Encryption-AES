from django.urls import path
from .views import index, encrypt_image, decrypt_image

urlpatterns = [
    path('', index, name='homepage'),
    path('encrypt/', encrypt_image, name='encrypt'),
    path('decrypt/', decrypt_image, name='decrypt'),
]
