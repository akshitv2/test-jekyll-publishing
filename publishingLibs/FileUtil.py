import base64
import os
import re


def get_links(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return []
    return os.listdir(folder_path)


def get_file_content(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        return content


def extract_md_header(text):
    # re.DOTALL (or re.S) makes the '.' match newline characters
    pattern = r"---(.*?)---"
    match = re.search(r'---\s*(.*?)\s*---', text, re.DOTALL)

    if match:
        extracted_text = match.group(1)
        return extracted_text
    else:
        return ''


def write_public_page(output_file,filename, file_content, iv, ct_bytes):
    with open(output_file, "w") as f:
        f.write(
            '---\n' + extract_md_header(file_content) + '\n---\n'
            + '# ' + filename.capitalize().replace(".md", "") + '\n' +
            '<div id="iv">' + str(iv) + '</div>' +
            '<div id="cipher">' + str(ct_bytes) + '</div>')

def convert_md_to_base64(file_content):
    # Convert string to bytes, then to base64
    content_bytes = file_content.encode("utf-8")
    base64_bytes = base64.b64encode(content_bytes)

    # Convert back to string for easier reading/JSON storage
    base64_string = base64_bytes.decode("utf-8")

    # print(f"Successfully processed: {filename}")
    return base64_string