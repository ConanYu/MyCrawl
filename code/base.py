import os
import requests
from lxml import etree
from bs4 import BeautifulSoup


def url_to_str(url):
	html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
	soup = BeautifulSoup(html.text, 'lxml')
	return soup.prettify()


def str_to_htm(s):
	return etree.HTML(s)


def url_to_htm(url):
	return str_to_htm(url_to_str(url))


def find_file_name(url):
	pos = 0
	for i, j in enumerate(url):
		if j == '/':
			pos = i
	return url[pos:]


path = os.getcwd() + '\\download'


def download(url):
	if not os.path.exists(path):
		os.makedirs(path)
	address = path + '\\' + find_file_name(url)
	if os.path.exists(address):
		raise FileExistsError
	with open(address, 'wb') as f:
		f.write(requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).content)
