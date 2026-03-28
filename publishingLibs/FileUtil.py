import os

def get_links(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return []
    return os.listdir(folder_path)

def get_file_content(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        return content