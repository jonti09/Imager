from bs4 import BeautifulSoup
import requests
import time

file = open('LinuxG.txt', 'a')
count = 1

for i in range(1, 10):

    url = 'http://linuxg.net/'

    if i > 1:
        url = 'http://linuxg.net/page/' + str(i)

    r = requests.get(url)

    if r.status_code == 200:

        soup = BeautifulSoup(r.content, 'html.parser')

        links = soup.find_all('h1', attrs={'class': 'post-title'})

        for link in links:
            info_link = link.find('a')

            print(str(count) + ':\nINFO : ' + info_link.contents[0] + '\nLINK : ' + info_link['href'] + '\n')
            file.write(str(count) + ':\nINFO : ' + info_link.contents[0] + '\nLINK : ' + info_link['href'] + '\n\n')
            count += 1

        time.sleep(2)

    else:
        exit(0)

file.close()
