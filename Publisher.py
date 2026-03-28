import base64
import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from publishingLibs.FileUtil import get_links
from publishingLibs.KeyUtil import get_key
from publishingLibs.mdConv import get_file_content, extract_text, convert_md_to_base64, download_main_content

original_folder = "./original"  # Change this to your path
output_folder = "./pages"  # Change this to your path
key = get_key().encode()[:32]  # Must be 16, 24, or 32 bytes
print(key)

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