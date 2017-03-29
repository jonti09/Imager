#!/usr/bin/env python3
import requests, re
from bs4 import BeautifulSoup as bs

# url = 'http://sv1.bia2dl.xyz/Series/Animation/Avatar%3A%20The%20Last%20Airbender/s' + str(i) + '/'

with open('links', 'w+') as file:
	for i in range(1, 4):
		url = 'http://sv1.bia2dl.xyz/Series/Animation/Avatar%3A%20The%20Last%20Airbender/s' + str(i) + '/'
		r = requests.get(url)
		soup = bs(r.text, 'html.parser')
		for j, link in enumerate(soup.find_all('a')):
			if re.findall(r'S\d+', link['href']):
				file.write(url + link['href'] + '\n')