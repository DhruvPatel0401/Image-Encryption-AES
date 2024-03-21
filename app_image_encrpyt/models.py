from django.db import models

class EncryptedImage(models.Model):
    encrypted_image = models.ImageField(upload_to='media/', null=True, blank=True)
    password = models.CharField(max_length=256)

