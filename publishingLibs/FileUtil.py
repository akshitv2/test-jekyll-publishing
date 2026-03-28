import os

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