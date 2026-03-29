import base64
import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from publishingLibs.FileUtil import get_file_content, write_public_page, convert_md_to_base64
from publishingLibs.CryptoUtil import get_key, encrypt
from publishingLibs.LogUtil import LogUtil
from publishingLibs.WebUtil import get_rendered_html

config = {
    'original_folder': "./original",  # Change this to your path
    'output_folder': "./pages",  # Change this to your path
    'key':get_key().encode()[:32],
    'log_level': 'INFO'
}
log = LogUtil(config["log_level"])

def change_dir_to_current_file():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    log.info(("Current working directory:", os.getcwd()))
change_dir_to_current_file()
print(os.getcwd())

for filename in os.listdir(config["original_folder"]):
    # get original content of file to store for easy recovery
    file_content = get_file_content(os.path.join(config["original_folder"], filename))
    log.debug(("File content:", file_content))
    # convert to base64 for simple easy format
    base64_string = convert_md_to_base64(file_content)
    log.debug(("Base 64 String:", base64_string))

    html_content_string = get_rendered_html('http://localhost:4000/original/', filename)
    log.debug(("Content string:", html_content_string))

    data = html_content_string + '<div id="b64Container">' + base64_string + '</div>'
    iv, ct_bytes = encrypt(config["key"], data)
    write_public_page(config["output_folder"], filename, file_content, iv, ct_bytes)
