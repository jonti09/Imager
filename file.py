#!/usr/bin/env python3
import os
with open('links', 'r') as file:
	links = file.read().split('\n')
	for link in links:
		os.system('youtube-dl ' + link)