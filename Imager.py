#!/usr/bin/python3

import requests
import urllib.request
import os
from bs4 import BeautifulSoup


def saveImage(link):
    url = 'http://www.hdwallpapers.in/'
    img = url + link.split('/')[-1]
    r = requests.get(img)

    soup = BeautifulSoup(r.content, 'html.parser')
    link = soup.find_all('a', attrs={'title': '1920 x 1080'})[0]
    img_url = url + link['href'].split('/')[-2] + '/' + link['href'].split('/')[-1]

    urllib.request.urlretrieve(img_url, img_url.split('/')[-1])


def main():
    url = 'http://www.hdwallpapers.in/'

    pages = int(input("No of pages: "))

    dirname = 'HDWallPaper'

    if not os.path.isdir(dirname):
        os.mkdir(dirname)
        os.chdir(dirname)

    else:
        os.chdir(dirname)

    for i in range(1, pages + 1):
        if i > 1:
            url = 'http://www.hdwallpapers.in/latest_wallpapers/page/' + str(i)

        r = requests.get(url)

        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            links = soup.find_all('div', attrs={'class': 'thumb'})

            for link in links:
                img_link = link.find('a')['href']
                print("Saving Image : " + str(link.find('p').text))
                saveImage(img_link)

        else:
            print("Some shit happened on " + str(i) + " page")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
