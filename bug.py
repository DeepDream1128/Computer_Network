import requests
from bs4 import BeautifulSoup
import re
import os

def download_pdf(url, folder="downloaded_pdfs"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve the page")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_links = soup.find_all('a', href=re.compile(r'/(details|download)/[^\s]+\.pdf'))

    if not os.path.exists(folder):
        os.makedirs(folder)

    for link in pdf_links:
        pdf_url = 'https://archive.org' + link.get('href')
        pdf_response = requests.get(pdf_url, headers=headers)
        pdf_name = pdf_url.split('/')[-1]

        with open(f"{folder}/{pdf_name}", 'wb') as file:
            file.write(pdf_response.content)
        print(f"Downloaded {pdf_name}")

download_pdf("https://archive.org/details/networking-books")
