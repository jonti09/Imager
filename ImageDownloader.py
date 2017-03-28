"""
	Author          :   Viper
	Version         :   1.0
	Description     :   This program downloads all the available Pictures in User defined resolution.
	Usage           :   i.  Type in number to select the operation.
						ii. Then select the resolution
"""
import requests
import os
import urllib.request
from bs4 import BeautifulSoup


class Imager():
	BASE_URL = 'http://www.hdwallpapers.in/'
	URL = BASE_URL
	COUNT = 0
	DOWN = 0
	SKIP = 0
	ERROR = 0

	UInput = {
		'url': '',
		'resolution': '',
		'dir': False,
		'pages': 10,
	}

	#URL
	OP = {
		1: 'celebrities-desktop-wallpapers/',
		2: '',
	}

	# the dictionary for multiple resolution
	RES = {
		1:  '640 x 1136', 2:  '750 x 1334', 3:  '640 x 1136', 4:  '750 x 1334', 5:  '1080 x 1920',
		6:  '360 x 640', 7:  '540 x 960', 8:  '720 x 1280', 9:  '1080 x 1920', 10: '480 x 800',
		11: '768 x 1280', 12: '1280 x 800', 13: '1440 x 900', 14: '1680 x 1050', 15: '1920 x 1200', 
		16: '2560 x 1600', 17: '2880 x 1800', 18: '1280 x 720', 19: '1366 x 768', 20: '1600 x 900',
		21: '1920 x 1080', 22: '2560 x 1440',
	}

	DIR = {
		1: False,
		2: True,
	}


	def __init__(self):
		# op to perform
		self.UInput['url'] = self.OP[int(input('''
What images to download??
	1. Of Celebrity
	2. All the Images
>>> '''))]

		if 'celebrities' in self.UInput['url']:
			self.UInput['dir'] = self.DIR[int(input('''
Want to make separate folders for all the Celebs:
1. NO
2. YES
>>> '''))]

	# the RES to consider
		self.UInput['resolution'] = self.RES[int(input('''
In What resolution:
	*** iPhone 5 5S resolutions ***
	1.  640 x 1136

	*** iPhone 6 6S resolutions ***
	2.  750 x 1334

	*** iPhone 6 6S Plus resolutions ***
	3.  640 x 1136

	*** Android Mobiles HD resolutions ***
	4.  750 x 1334\t\t5.  1080 x 1920
	6.  360 x 640\t\t7.  540 x 960 
	8.  720 x 1280\t\t9.  1080 x 1920

	*** Mobiles HD resolutions ***
	10. 480 x 800\t\t11. 768 x 1280

	*** Widescreen resolutions ***
	12. 1280 x 800\t\t13. 1440 x 900 
	14. 1680 x 1050\t\t15. 1920 x 1200 
	16. 2560 x 1600

	*** Retina Wide resolutions ****
	17. 2880 x 1800

	*** HD resolutions ***
	18. 1280 x 720\t\t19. 1366 x 768 
	20. 1600 x 900\t\t21. 1920 x 1080
	22. 2560 x 1440
>>> '''))]

		pages = input('''
Specify No of pages to download (leave empty for default = 10)
NOTE: Each page has 14 Images
>>> ''')

		if not pages:
			self.UInput['pages'] = 10
		else:
			self.UInput['pages'] = int(pages)


	# Function check if directory exists or not
	def makeDir(self, dirname):
		if not os.path.isdir(dirname):
			os.mkdir(dirname)
			os.chdir(dirname)
		else:
			os.chdir(dirname)


	# Function saves the image in the directory from the given url
	def saveImage(self, link):
		# get the href link
		img = self.BASE_URL + link.split('/')[-1]
		r = requests.get(img)

		# parse the link
		soup = BeautifulSoup(r.content, 'html.parser')

		# find the url of given RES image size
		try:
			link = soup.find_all('a', attrs={'title': str(self.UInput['resolution'])})[0]

			# get the image_url and img_name from the generated link
			
			img_url = self.BASE_URL + link['href'].split('/')[-2] + '/' + link['href'].split('/')[-1]
			img_name = img_url.split('/')[-1]

			# download image if does not exist else skip it
			if not os.path.exists(img_name):
				try:
					# actully save image
					urllib.request.urlretrieve(img_url, img_name)
					print('saved...')
					self.DOWN += 1
				except KeyboardInterrupt:
					print('Exiting...')
					input('Press ENTER to exit...')
					exit(0)
				except:
					# if some shit occure...this helps...
					self.ERROR += 1
					print('Some Error occured...')
			else:
				self.SKIP += 1
				print('Already Exists, Skipping it...')
		except IndexError:
			self.ERROR += 1
			print('List Index Error...')
		except Exception as e:
			self.ERROR += 1
			print('No image available...')
			

	def main(self):
		# make the Folder for Images
		self.makeDir("Imager")

		# append the selected op to URL
		self.URL += self.UInput['url']
		for i in range(1, self.UInput['pages'] + 1):
			# Change the URL on each iteration
			self.URL += 'page/' + str(i)
			print(self.URL)
			req = requests.get(self.URL)

			# if the requests is successful, then continue else show error and exit
			if req.status_code == 200:
				# get the whole page
				s = BeautifulSoup(req.content, 'html.parser')

				# find all the links relevant to us and iterate over it
				for celeb in s.find_all('div', attrs={'class': 'thumb'}):
					# get the name and link of the image
					celeb_link = celeb.find('a')
					celeb_name = celeb_link.find('p').text

					# If separete dir, then make else continue....
					dirname = celeb_name.split(' ')[0] + ' ' + celeb_name.split(' ')[1]
					if self.UInput['dir']:
						self.makeDir(dirname)
					self.COUNT += 1
					print('(%s) Saving %s ...' % (self.COUNT, dirname), end='  ')

					# Save image
					self.saveImage(celeb_link['href'])
					if self.UInput['dir']:
						os.chdir('..')

			else:
				print('Some error occured with %d code...exiting...' % req.status_code)
				input('Enter any key to exit...')
				exit(1)


print('Press ctrl + c to exit...')
try:
	obj = Imager()
	obj.main()
	print('%d Pics processed from which : \n%d Downloaded...,\n%d Skipped...\n%d had Error...' % (obj.COUNT, obj.DOWN, obj.SKIP, obj.ERROR))
except ValueError:
	print('Did not provide correct value....exiting...')
	input('Press any key to exit...')
	exit(1)	
except KeyboardInterrupt:
	print('Exiting...')
	input('Press any key to exit...')
	exit(0)
		
