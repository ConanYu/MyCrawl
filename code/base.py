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
