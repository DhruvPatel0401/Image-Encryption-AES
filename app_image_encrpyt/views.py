from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImageForm
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from PIL import Image
import io
import base64
from django.http import FileResponse

def index(request):
    return render(request, 'index.html')

def encrypt_image(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        image = request.FILES.get('image')
        
        # Hash the password to generate a 256-bit key
        hashed_password = SHA256.new(password.encode()).digest()
        
        # Encryption process
        aes_cipher = AES.new(hashed_password, AES.MODE_ECB)
        img_bytes = image.read()
        padded_img_bytes = img_bytes + bytes((AES.block_size - len(img_bytes) % AES.block_size) * chr(AES.block_size - len(img_bytes) % AES.block_size), 'utf-8')
        encrypted_img = aes_cipher.encrypt(padded_img_bytes)

        encoded_img_data = base64.b64encode(encrypted_img)
        encoded_img_bytes = encoded_img_data.decode('utf-8').encode('utf-8')

        return HttpResponse(encoded_img_bytes, content_type='text/plain')

def decrypt_image(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        image = request.FILES.get('image')
        
        # Hash the password to generate a 256-bit key
        hashed_password = SHA256.new(password.encode()).digest()
        
        # Decryption process
        aes_cipher = AES.new(hashed_password, AES.MODE_ECB)
        decrypted_img_bytes = aes_cipher.decrypt(image.read())

        # Remove padding from decrypted bytes
        padding_length = decrypted_img_bytes[-1]
        decrypted_img_bytes = decrypted_img_bytes[:-padding_length]

        # Create an image from decrypted bytes
        img = Image.open(io.BytesIO(decrypted_img_bytes))
        img = img.convert('RGB')
        response = HttpResponse(content_type='image/jpeg')
        img.save(response, format='JPEG')
        response['Content-Disposition'] = 'attachment; filename=decrypted_image.jpg'

        return response