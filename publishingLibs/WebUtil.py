import requests
from bs4 import BeautifulSoup


def get_rendered_html(url, filename):
    filename = filename.replace('.md', '')
    try:
        # 1. Fetch the webpage content
        headers = {'User-Agent': 'Mozilla/5.0'}  # Pretend to be a browser
        response = requests.get(url+filename, headers=headers)
        response.raise_for_status()  # Check for HTTP errors

        # 2. Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. Locate the specific <main> tag
        # We use a dictionary to match multiple attributes exactly
        main_content = soup.find('div', {
            'id': 'main-content'
        })

        if main_content:
            return str(main_content)

    except Exception as e:
        print(f"An error occurred: {e}")