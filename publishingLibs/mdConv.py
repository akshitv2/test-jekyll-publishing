import os
import base64
import re
import sys

import requests
from bs4 import BeautifulSoup
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import json


def get_links(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return []

    files = [
        f.replace(".md", "")
        for f in os.listdir(folder_path)
        if f.endswith(".md")
    ]

    print(files)
    return files

def download_main_content(url):
    try:
        # 1. Fetch the webpage content
        headers = {'User-Agent': 'Mozilla/5.0'}  # Pretend to be a browser
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors

        # 2. Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. Locate the specific <main> tag
        # We use a dictionary to match multiple attributes exactly
        main_content = soup.find('div', {
            'id': 'main-content'
        })
        print(main_content)

        if main_content:
            return str(main_content)
            # 4. Save the content to a file
        #     with open(output_file, 'w', encoding='utf-8') as f:
        #         f.write(str(main_content))
        #     print(f"Successfully saved content to {output_file}")
        # else:
        #     print("Could not find the specified <main> tag on this page.")

    except Exception as e:
        print(f"An error occurred: {e}")


def get_file_content(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        return content


def convert_md_to_base64(file_content):
    # Convert string to bytes, then to base64
    content_bytes = file_content.encode("utf-8")
    base64_bytes = base64.b64encode(content_bytes)

    # Convert back to string for easier reading/JSON storage
    base64_string = base64_bytes.decode("utf-8")

    # print(f"Successfully processed: {filename}")
    return base64_string


def get_key():
    try:
        # 1. Fetch the webpage content
        headers = {'User-Agent': 'Mozilla/5.0'}  # Pretend to be a browser
        response = requests.get('http://localhost:4000/key/key', headers=headers)
        response.raise_for_status()  # Check for HTTP errors

        # 2. Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. Locate the specific <main> tag
        # We use a dictionary to match multiple attributes exactly
        main_content = soup.find('div', {
            'id': 'keyholder'
        })
        print(main_content)

        if main_content:
            return str(main_content).replace('<div id="keyholder">', '').replace('</div>', '')
            # 4. Save the content to a file

    except Exception as e:
        print(f"An error occurred: {e}")


def extract_text(text):
    # re.DOTALL (or re.S) makes the '.' match newline characters
    pattern = r"---(.*?)---"
    match = re.search(r'---\s*(.*?)\s*---', text, re.DOTALL)

    if match:
        extracted_text = match.group(1)
        return extracted_text
    else:
        return ''


if __name__ == '__main__':
    # Configuration
    key = get_key().encode()[:32]  # Must be 16, 24, or 32 bytes
    print(key)
    # Usage
    original_folder = "./original"  # Change this to your path
    output_folder = "./pages"  # Change this to your path

    for filename in get_links(original_folder):
        file_content = get_file_content(os.path.join(original_folder, filename + ".md"))
        print("Extracted : ", extract_text(file_content))
        base64_string = convert_md_to_base64(file_content)
        print(base64_string)

        target_url = 'http://localhost:4000/original/' + filename
        content_string = download_main_content(target_url)
        print(content_string)

        data = content_string + '<div id="b64Container">' + base64_string + '</div>'

        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        result = {
            'iv': base64.b64encode(iv).decode('utf-8'),
            'ciphertext': base64.b64encode(ct_bytes).decode('utf-8')
        }
        print(os.path.join(output_folder, filename.capitalize() + '.md'))

        with open(os.path.join(output_folder, filename.capitalize() + '.md'), "w") as f:
            f.write('---\n' + extract_text(file_content) + '\n---\n' + '# ' + filename.capitalize() + '\n' +
                    '<div id="iv">' + str(result['iv']) + '</div>' +
                    '<div id="cipher">' + str(result['ciphertext']) + '</div>')
