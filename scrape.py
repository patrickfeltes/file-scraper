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

def get_all_images(url):
    data = get_link_data(url)
    text = data.decode('utf-8')
    soup = BeautifulSoup(text, 'html.parser')
    return list(map(lambda x : x.get('src'), soup.find_all('img')))

def get_all_files(url):
    return get_all_links(url) + get_all_images(url)

def get_all_extension_links(url, extensions):
    links = get_all_files(url)
    lst = []
    for exten in extensions:
        for link in links:
            if link.endswith(exten):
                lst.append(link)
    return lst

def download_all_files(url, folder, extensions):
    try:
        os.makedirs(folder)
    except:
        pass

    links = get_all_extension_links(url, extensions)

    for link in links:
        filename = link[link.rfind('/') + 1:]
        actual_filename = os.path.join(folder, filename)

        with open(actual_filename, 'wb') as f:
            # if the link is relative, join it with the initial url
            if not link.startswith('http'):
                link = urljoin(url, link)

            print('Downloading:', link)
            data = urlopen(link).read()
            f.write(data)

if __name__ == '__main__':
    url = input('Please enter a url to scrape: ')
    folder = input('Enter a folder name to save files in. If you want the current folder, press enter. ')
    extensions = input('Enter file extensions to download as a comma separated list (ex: pdf, png, jpg) ')
    extensions = extensions.split(',')
    # remove periods from the beginning of file extensions if they exist
    extensions = list(map(lambda x: x[1:].strip() if x[0] == '.' else x.strip(), extensions))

    download_all_files(url, folder, extensions)