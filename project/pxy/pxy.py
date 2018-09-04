import requests
from lxml import etree
from bs4 import BeautifulSoup
user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
URL = 'http://www.goubanjia.com/'


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
			raise ConnectionError(URL + ' status code: ' + str(html.status_code))
	return BeautifulSoup(html.text, 'lxml')


def clear(s):
	ret = ''
	for i in s:
		if i != ' ' and i != '\n':
			ret += i
	return ret


def find(html):
	obj = etree.HTML(html)
	result = obj.xpath('//text()')
	ret = ''
	for i in result:
		ret += clear(i)
	return ret


def get_proxy(proxy=None):
	# we can use proxy to get proxies.
	arr = url_to_soup(URL, proxy).find_all(name='td', attrs={'class': 'ip'})
	ret = []
	for i in arr:
		[j.extract() for j in i.find_all(attrs={'style': 'display: none;'})]
		[j.extract() for j in i.find_all(attrs={'style': 'display:none;'})]
		ret.append(find(i.prettify()))
	return ret


if __name__ == '__main__':
	import random
	arr = get_proxy()
	arr = get_proxy(random.sample(arr, 1)[0])
	print(arr)
