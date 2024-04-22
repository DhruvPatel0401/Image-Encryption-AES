from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response  import Response
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import base64
from PIL import Image
import io

@api_view(['POST'])
def encrypt_image(request):
    if 'image' not in request.FILES or 'password' not in request.data:
        return Response({'error': 'Image and password are required.'}, status=400)

    image_file = request.FILES['image']
    password = request.data['password']
    IV = b'\x00' * 16 

     # Hash the password to generate a 256-bit key
    hasher = SHA256.new()
    hasher.update(password.encode('utf-8'))
    key = hasher.digest()

    im = Image.open(io.BytesIO(image_file.read()))
    im = im.convert('RGB')
    data = im.tobytes()
    original_data = len(data)
    
    aes = AES.new(key, AES.MODE_CBC, IV) 
    encrypted_data = aes.encrypt(pad(data)[:original_data])

    # Convert the encrypted data back to RGB pixels
    encrypted_im = Image.new(im.mode, im.size)
    encrypted_im.putdata(convert_to_RGB(encrypted_data))
    
    # Convert the encrypted image back to bytes
    buffer = io.BytesIO()
    encrypted_im.save(buffer, format='PNG')
    encrypted_image_bytes = buffer.getvalue()

    # Encode the encrypted image bytes in Base64
    encrypted_image_base64 = base64.b64encode(encrypted_image_bytes).decode('utf-8')

    return Response({'encrypted_image': encrypted_image_base64})


@api_view(['POST'])
def decrypt_image(request):
    if 'image' not in request.FILES or 'password' not in request.data:
        return Response({'error': 'Image and password are required.'}, status=400)
    
    image_file = request.FILES['image']
    password = request.data['password']
    IV = b'\x00' * 16

    # Hash the password to generate a 256-bit key
    hasher = SHA256.new()
    hasher.update(password.encode('utf-8'))
    key = hasher.digest()

    im = Image.open(io.BytesIO(image_file.read()))
    im = im.convert('RGB')
    data = im.tobytes()
    original_data = len(data)

    aes = AES.new(key, AES.MODE_CBC, IV)
    decrypted_data = aes.decrypt(pad(data)[:original_data])

    # Convert the decrypted data back to RGB pixels
    decrypted_im = Image.new(im.mode, im.size)
    decrypted_im.putdata(convert_to_RGB(decrypted_data))

    # Convert the decrypted image back to bytes
    buffer = io.BytesIO()
    decrypted_im.save(buffer, format='PNG')
    decrypted_image_bytes = buffer.getvalue()

    # Encode the decrypted image bytes in Base64
    decrypted_image_base64 = base64.b64encode(decrypted_image_bytes).decode('utf-8')

    return Response({'decrypted_image': decrypted_image_base64})

def pad(data): 
    return data + b"\x00"*(16-len(data)%16)

def convert_to_RGB(data): 
    r, g, b = tuple(map(lambda d: [data[i] for i in range(0, len(data)) if i % 3 == d], [0, 1, 2])) 
    pixels = tuple(zip(r,g,b)) 
    return pixels 

  