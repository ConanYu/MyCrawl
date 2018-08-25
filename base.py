import requests
from bs4 import BeautifulSoup


def url_to_str(url):
	html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
	soup = BeautifulSoup(html.text, 'lxml')
	return soup.prettify()
