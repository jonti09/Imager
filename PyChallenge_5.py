import requests
import re
from bs4 import BeautifulSoup

url = 'http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing='
next = 12345

reg = re.compile(r'the next nothing is \d+')

i = 1

while True:
	try:
		print(str(i) + ' : ' + str(next))

		r = requests.get(url + str(next))
		soup = BeautifulSoup(r.content, 'html.parser')
		next = int(reg.findall(str(soup))[0].split(' ')[-1])
	
	except IndexError: 
		try:
			if re.compile(r'Divide by two').findall(str(soup))[0] != None:
				next //= 2
				print(str(i) + ' : ' + str(next))

		except IndexError:
			print('your Answer is : ' + str(soup))
			break
		
		reg = re.compile(r'the next nothing is \d+')

	i += 1
