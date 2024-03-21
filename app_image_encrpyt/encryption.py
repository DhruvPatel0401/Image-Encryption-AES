from PIL import Image

def encrypt_image(image_file_path, key, iv):
	cfb_cipher = AES.new(key, AES.MODE_CFB, iv)
	enc_data = cfb_cipher.encrypt(input_data)

	enc_file = open(filepath+"/encrypted.enc", "wb")
	enc_file.write(enc_data)
	enc_file.close()

def decrypt_image(encrypted_image_file, password):
    pass