import os
import requests
from lxml import etree
from bs4 import BeautifulSoup
user_agent = 'Mozilla/5.0'


def url_to_soup(url, proxy=None, f=False):
	header = {'User-agent': user_agent}
	if proxy is not None:
		header['proxy'] = proxy
	html = requests.get(url, headers=header)
	# if wrong then try again
	if html.status_code != 200:
		if not f:
			return url_to_soup(url, True)
		else:
			raise ConnectionError(url + ' status code: ' + str(html.status_code))
	return BeautifulSoup(html.text, 'lxml')


def url_to_str(url, proxy=None):
	soup = url_to_soup(url, proxy)
	return soup.prettify()


def str_to_htm(s):
	return etree.HTML(s)


def url_to_htm(url, proxy=None):
	return str_to_htm(url_to_str(url, proxy))


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
	obj = requests.get(url, headers={'User-agent': user_agent})
	if obj.status_code == 403:
		raise ConnectionRefusedError
	elif obj.status_code != 200:
		raise ConnectionError
	with open(address, 'wb') as f:
		f.write(obj.content)

