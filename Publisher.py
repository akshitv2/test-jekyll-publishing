import base64
import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from publishingLibs.FileUtil import get_file_content
from publishingLibs.KeyUtil import get_key
from publishingLibs.LogUtil import LogUtil
from publishingLibs.mdConv import extract_text, convert_md_to_base64, download_main_content, output_folder

config = {
    'original_folder': "./original",  # Change this to your path
    'output_folder': "./pages",  # Change this to your path
    'key':get_key().encode()[:32],
    'log_level': 'DEBUG'
}
log = LogUtil(config["log_level"])

def change_dir_to_current_file():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    log.info(("Current working directory:", os.getcwd()))
change_dir_to_current_file()
print(os.getcwd())

for filename in os.listdir(config["original_folder"]):
    file_content = get_file_content(os.path.join(config["original_folder"], filename))
    log.debug(("File content:", file_content))
    log.debug(("Extracted : ", extract_text(file_content)))
    base64_string = convert_md_to_base64(file_content)

    target_url = 'http://localhost:4000/original/' + filename
    content_string = download_main_content(target_url)
    log.debug(("Content string:", content_string))

    data = content_string + '<div id="b64Container">' + base64_string + '</div>'
#
    cipher = AES.new(config['key'], AES.MODE_CBC)
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
