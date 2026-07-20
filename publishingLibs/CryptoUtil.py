import base64

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from bs4 import BeautifulSoup


def get_key():
    try:
        # 1. Fetch the webpage content
        headers = {'User-Agent': 'Mozilla/5.0'}  # Pretend to be a browser
        response = requests.get('http://localhost:4000/key/key', headers=headers)
        response.raise_for_status()  # Check for HTTP errors

        # 2. Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. Locate the specific <div> tag with key id
        main_content = soup.find('div', {
            'id': 'keyholder'
        })

        if main_content:
            return str(main_content).replace('<div id="keyholder">', '').replace('</div>', '')
            # 4. Save the content to a file

    except Exception as e:
        print(f"An error occurred: {e}")

def encrypt(key, data):
    iv = b"1234567890123456"
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(iv).decode('utf-8'),base64.b64encode(ct_bytes).decode('utf-8')