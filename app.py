# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# Create a Flask app
app = Flask(__name__)

# Define the correct username and password
valid_username = "musa"
valid_password = "musa"

# AES encryption function
def encrypt_text(key, plaintext):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return ciphertext, cipher.iv

# AES decryption function
def decrypt_text(key, ciphertext, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

# Generate a random 256-bit AES key
key = get_random_bytes(32)

# Define the route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == valid_username and password == valid_password:
            # If the username and password match, redirect to index.html
            return redirect(url_for('home'))
        else:
            # If the credentials are incorrect, show an error message
            error_message = "Invalid username or password. Please try again."
            return render_template('login.html', error=error_message)
    
    return render_template('login.html', error=None)

# Define the route for the home page (index.html)
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        key = request.form['key']
        key = key.ljust(32)[:32].encode('utf-8')
        if 'encrypt' in request.form:
            plaintext = request.form['text']
            ciphertext, iv = encrypt_text(key, plaintext)
            return render_template('index.html', encrypted=ciphertext.hex(), iv=iv.hex(), text=plaintext)
        elif 'decrypt' in request.form:
            ciphertext = bytes.fromhex(request.form['encrypted'])
            iv = bytes.fromhex(request.form['iv'])
            decrypted_text = decrypt_text(key, ciphertext, iv)
            return render_template('index.html', decrypted=decrypted_text, text=request.form['text'], encrypted=ciphertext.hex(), iv=iv.hex())
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)



