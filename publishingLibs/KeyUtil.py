import requests
from bs4 import BeautifulSoup


def get_key():
    try:
        # 1. Fetch the webpage content
        headers = {'User-Agent': 'Mozilla/5.0'}  # Pretend to be a browser
        response = requests.get('http://localhost:4000/key/key', headers=headers)
        response.raise_for_status()  # Check for HTTP errors

        # 2. Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. Locate the specific <div> tag with key id
        main_content = soup.find('div', {
            'id': 'keyholder'
        })

        if main_content:
            return str(main_content).replace('<div id="keyholder">', '').replace('</div>', '')
            # 4. Save the content to a file

    except Exception as e:
        print(f"An error occurred: {e}")