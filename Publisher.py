import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from publishingLibs.CryptoUtil import encrypt, get_key
from publishingLibs.FileUtil import (
    convert_md_to_base64,
    get_file_content,
    get_img_content,
    write_public_image,
    write_public_page,
)
from publishingLibs.LogUtil import LogUtil
from publishingLibs.WebUtil import get_rendered_html

config = {
    'original_folder': "./original",
    'output_folder': "./pages",
    'key': get_key().encode()[:32],
    'iv': b"1234567890123456",
    'log_level': 'INFO',
    'process_md': True
}
log = LogUtil(config["log_level"])

def change_dir_to_current_file():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    log.info(("Current working directory:", os.getcwd()))

change_dir_to_current_file()

directory = Path(config["original_folder"])
output_directory = Path(config["output_folder"])

def process_file(file_path: Path):
    if not file_path.is_file():
        return

    output_dir = output_directory.joinpath(file_path.parent.relative_to(directory))
    os.makedirs(output_dir, exist_ok=True)
    filename = file_path.name

    if filename.endswith(".md"):
        file_content = get_file_content(file_path)
        log.debug(("File content:", file_content))

        base64_string = convert_md_to_base64(file_content)
        log.debug(("Base 64 String:", base64_string))

        html_content_string = get_rendered_html('http://localhost:4000/original/', str(file_path.relative_to(directory)))
        log.debug(("Content string:", html_content_string))

        data = html_content_string + '<div id="b64Container">' + base64_string + '</div>'
        iv, ct_bytes = encrypt(config["key"], config["iv"], data)
        output_file = str(output_directory.joinpath(file_path.relative_to(directory)))
        log.debug(("Output file:", output_file))
        write_public_page(output_file, filename, file_content, iv, ct_bytes)

    elif filename.endswith(".png") or filename.endswith(".gif"):
        file_content = get_img_content(file_path)
        iv, ct_bytes = encrypt(config["key"], config["iv"], file_content)
        output_file = str(output_directory.joinpath(file_path.relative_to(directory)))
        log.debug(("Output file:", output_file))
        write_public_image(output_file, iv, ct_bytes)

if config["process_md"]:
    files = [f for f in directory.rglob("*") if f.is_file()]
    max_workers = 16  # Adjust based on local server capacity

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        list(executor.map(process_file, files))