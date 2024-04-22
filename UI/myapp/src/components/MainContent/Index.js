import React, { useState } from 'react';
import './Index.css';

function Index() {
  const [image, setImage] = useState(null);
  const [password, setPassword] = useState('');
  const [encryptedImage, setEncryptedImage] = useState(null);
  const [decryptedImage, setDecryptedImage] = useState(null);
  const [error, setError] = useState('');

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const validateFields = () => {
    if (!image) {
      setError('Please select an image.');
      return false;
    }
    if (!password.trim()) {
      setError('Please enter a password.');
      return false;
    }
    setError('');
    return true;
  };

  const handleEncrypt = () => {
    if (validateFields()) {
      const formData = new FormData();
      formData.append('image', image);
      formData.append('password', password);

      fetch('http://127.0.0.1:8000/api/encrypt/', {
        method: 'POST',
        body: formData
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to encrypt the image.');
          }
          return response.json();
        })
        .then(data => {
          const binaryString = window.atob(data.encrypted_image); // Decode the Base64 string
          const len = binaryString.length;
          const bytes = new Uint8Array(len);
          for (let i = 0; i < len; i++) {
            bytes[i] = binaryString.charCodeAt(i);
          }

          // Create a Blob from the ArrayBuffer
          const blob = new Blob([bytes.buffer], { type: 'image/png' });

          // Create a URL for the Blob
          const url = window.URL.createObjectURL(blob);

          // Create a link element
          const a = document.createElement('a');
          a.href = url;
          a.download = 'encrypted_image.png'; // Set the download attribute to specify the filename
          document.body.appendChild(a); // Append the link to the body
          a.click(); // Click the link to trigger the download
          window.URL.revokeObjectURL(url); // Release the object URL
        })
        .catch(error => {
          console.error('Error:', error);
          setError('An error occurred while encrypting the image.');
        });
    }
  };


  const handleDecrypt = () => {
    if (validateFields()) {
      const formData = new FormData();
      formData.append('image', image);
      formData.append('password', password);

      fetch('http://127.0.0.1:8000/api/decrypt/', {
        method: 'POST',
        body: formData
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to decrypt the image.');
        }
        return response.json(); // Convert response to Blob object
      })
      .then(data => {
        const binaryString = window.atob(data.decrypted_image); // Decode the Base64 string
        const len = binaryString.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
          bytes[i] = binaryString.charCodeAt(i);
        }

        // Create a Blob from the ArrayBuffer
        const blob = new Blob([bytes.buffer], { type: 'image/png' });

        // Create a URL for the Blob
        const url = window.URL.createObjectURL(blob);

        // Create a link element
        const a = document.createElement('a');
        a.href = url;
        a.download = 'decrypted_image.png'; // Set the download attribute to specify the filename
        document.body.appendChild(a); // Append the link to the body
        a.click(); // Click the link to trigger the download
        window.URL.revokeObjectURL(url); // Release the object URL
      })
      .catch(error => {
        console.error('Error:', error);
        setError('An error occurred while decrypting the image.');
      });
    }
  };

  return (
    <main className='index'>
      <div className="input-container">
        <input type="file" accept=".jpeg, .jpg, .png" onChange={handleImageChange} />
        <input type="password" placeholder="Enter password" value={password} onChange={handlePasswordChange} />
      </div>
      {error && <p className="error">{error}</p>}
      <div className="button-container">
        <button onClick={handleEncrypt}>Encrypt Image</button>
        <button onClick={handleDecrypt}>Decrypt Image</button>
      </div>
      {encryptedImage && <div className="image-container"><img src={URL.createObjectURL(encryptedImage)} alt="Encrypted Image" /></div>}
      {decryptedImage && <div className="image-container"><img src={URL.createObjectURL(decryptedImage)} alt="Decrypted Image" /></div>}
    </main>
  );
}

export default Index;
