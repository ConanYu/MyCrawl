import os
import requests
from lxml import etree
from bs4 import BeautifulSoup


def url_to_soup(url):
	html = requests.get(url, headers={'User-agent': 'Chrome/63.0.3239.108'})
	return BeautifulSoup(html.text, 'lxml')


def url_to_str(url):
	soup = url_to_soup(url)
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
	obj = requests.get(url, headers={'User-agent': 'Chrome/63.0.3239.108'})
	if obj.status_code == 403:
		raise ConnectionRefusedError
	elif obj.status_code != 200:
		raise ConnectionError
	with open(address, 'wb') as f:
		f.write(obj.content)

