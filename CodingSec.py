import requests
import time
from bs4 import BeautifulSoup

file = open('CodingSec.txt', 'a')
count = 1

for i in range(1, 5):
    url = 'https://codingsec.net/'

    if i > 1:
        url += '/page' + str(i)

    r = requests.get(url)

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')

        links = soup.find_all('h2', attrs={'class': 'title'})

        for link in links:
            link_info = link.find('a')

            print(str(count) + "\nINFO: " + link_info.contents[0] + "\nLINK: " + link_info['href'] + '\n')
            file.write(str(count) + "\nINFO: " + link_info.contents[0] + "\nLINK: " + link_info['href'] + '\n\n')
            count += 1

        time.sleep(2)
    else:
        exit(0)

file.close()
