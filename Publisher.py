import base64
import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from tqdm import tqdm


from publishingLibs.FileUtil import get_file_content, write_public_page, convert_md_to_base64, get_img_content, \
    write_public_image
from publishingLibs.CryptoUtil import get_key, encrypt
from publishingLibs.LogUtil import LogUtil
from publishingLibs.WebUtil import get_rendered_html
import json

config = {
    'original_folder': "./original",  # Change this to your path
    'output_folder': "./pages",  # Change this to your path
    'key':get_key().encode()[:32],
    'log_level': 'INFO',
    'media_json_input': 'original/media.json',
    'media_json_output': 'pages/media.json',
    'process_md': True
}
log = LogUtil(config["log_level"])

def change_dir_to_current_file():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    log.info(("Current working directory:", os.getcwd()))
change_dir_to_current_file()

from pathlib import Path

directory = Path(config["original_folder"])
output_directory = Path(config["output_folder"])
files = list(directory.rglob("*"))

if config["process_md"]:
    for file_path in tqdm(files):
        output_dir = output_directory.joinpath(file_path.parent.relative_to(directory))
        os.makedirs(output_dir, exist_ok=True)
        filename = file_path.name
        if filename.endswith(".md"):
            # get original content of file to store for easy recovery
            file_content = get_file_content(file_path)
            log.debug(("File content:", file_content))
            # convert to base64 for simple easy format
            base64_string = convert_md_to_base64(file_content)
            log.debug(("Base 64 String:", base64_string))

            html_content_string = get_rendered_html('http://localhost:4000/original/', str(file_path.relative_to(directory)))
            log.debug(("Content string:", html_content_string))

            data = html_content_string + '<div id="b64Container">' + base64_string + '</div>'
            iv, ct_bytes = encrypt(config["key"], data)
            output_file = str((output_directory.joinpath(file_path.relative_to(directory))))
            log.debug(("Output file:", output_file))
            write_public_page(output_file, filename, file_content, iv, ct_bytes)
        if filename.endswith(".png"):
            file_content = get_img_content(file_path)
            iv, ct_bytes = encrypt(config["key"], file_content)
            output_file = str((output_directory.joinpath(file_path.relative_to(directory))))
            log.debug(("Output file:", output_file))
            write_public_image(output_file,iv,ct_bytes)

with open(config['media_json_input'], 'r') as f:
    data = json.load(f)
lowercase_data = {k: encrypt(config["key"], v) for k, v in data.items()}
with open(config['media_json_output'], 'w') as f:
    json.dump(lowercase_data, f, indent=4)
