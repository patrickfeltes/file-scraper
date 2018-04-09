from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
import os

def get_link_data(url):
    return urlopen(url).read()

def get_all_links(url):
    data = get_link_data(url)
    text = data.decode('utf-8')
    soup = BeautifulSoup(text, 'html.parser')
    return list(map(lambda x : x.get('href'), soup.find_all('a')))

def get_all_pdf_links(url):
    links = get_all_links(url)
    return list(filter(lambda s : s.endswith('.pdf'), links))

def download_all_pdfs(url, folder):
    # try to make a folder, don't make it if it's already there
    try:
        os.makedirs(folder)
    except OSError:
        pass

    pdf_links = get_all_pdf_links(url)
    
    for link in pdf_links:
        filename = link[link.rfind('/') + 1:]
        with open(os.path.join(folder, filename), 'wb') as f:
            # if the link is relative, join it with the initial url
            if not link.startswith('http'):
                link = urljoin(url, link)

            print('Downloading:', link)
            data = get_link_data(link)
            f.write(data)

if __name__ == '__main__':
    url = input('Please enter a url to scrape: ')
    folder = input('Enter a folder name to save files in. If you want the current folder, press enter.')
    download_all_pdfs(url, folder)