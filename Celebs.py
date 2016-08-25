##!/usr/bin/python3

import requests
import urllib.request
import os
from bs4 import BeautifulSoup

url = 'http://www.hdwallpapers.in/'

#
# Function check if directory exists or not
#
def makeDir(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
        os.chdir(dirame)

    else:
        os.chdir(dirname)


#
# Function saves the image in the directory from the given url
#
def saveImage(link, down_count, sk_count):
    # get the href link
    img = url + link.split('/')[-1]
    r = requests.get(img)

    # parse the link
    soup = BeautifulSoup(r.content, 'html.parser')

    # find the url of 1920 * 1080 image size
    try:
        link = soup.find_all('a', attrs={'title': '1920 x 1080'})[0]

        # get the image_url and img_name from the generated link
        img_url = url + link['href'].split('/')[-2] + '/' + link['href'].split('/')[-1]
        img_name = img_url.split('/')[-1]

        # download image if does not exist else skip it
        if not os.path.exists(img_name):
            urllib.request.urlretrieve(img_url, img_name)
            down_count += 1
            print()

        else:
            sk_count += 1
            print('Already Exists, Skipping it...')
    except:
        print('No image available...')
        pass

def main(down_count, sk_count):
    # make the initial directory
    makeDir("Celebs")

    # create a payload to send to server
    
    # scrap all the pages
    count = 0
    for i in range(10, 236):
        # change the url from second page onwards
        if i == 1:
            req = requests.get(url + 'celebrities-desktop-wallpapers.html')

        else:
            req = requests.get(url + 'celebrities-desktop-wallpapers/page/' + str(i))

        # if the requests is successful, then continue else continue
        if req.status_code == 200:
            # get the whole page
            s = BeautifulSoup(req.content, 'html.parser')

            # find all the links relevant to us and iterate over it
            for celeb in s.find_all('div', attrs={'class': 'thumb'}):
                # get the name and link of the image
                celeb_link = celeb.find('a')
                celeb_name = celeb_link.find('p').text
                #print(celeb_link)

                # make the directory and save the image
                dirname = celeb_name.split(' ')[0] + ' ' + celeb_name.split(' ')[1]
                #makeDir(dirname)
                count += 1
                print('(%s) Saving pics of %s ...' % (count, dirname), end='  ')

                saveImage(celeb_link['href'], down_count, sk_count)   

                #os.chdir('..')

if __name__ == '__main__':
    try:
        down_count = 0
        sk_count = 0
        main(down_count, sk_count)
        print('%d Pics downloaded and %d skipped...' % (down_count, sk_count))

    except KeyboardInterrupt:
        exit()
