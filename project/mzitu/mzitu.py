import os
import random
import requests
from time import clock
from lxml import etree
from pxy import get_proxy
from bs4 import BeautifulSoup
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'
proxy = get_proxy()


def url_to_soup(url):
	html = requests.get(url, headers={'User-agent': user_agent, 'proxies': random.sample(proxy, 1)[0]})
	return BeautifulSoup(html.text, 'lxml')


def url_to_str(url):
	soup = url_to_soup(url)
	return soup.prettify()


def find_file_name(url):
	"""
	find the file name from the url
	for example:
		url: https://www.baidu.com/robots.txt
		file name: robots.txt
	"""
	pos = 0
	for i, j in enumerate(url):
		if j == '/':
			pos = i
	return url[pos + 1:]


st = set('?*/\\<>:\"|')
# prevent os Error
def clear_dir(obj):
	ret = ''
	for i in obj:
		if i not in st:
			ret += i
	return ret


# where you want to download to
path = 'D:\\mzitu'
def download(url, title, referer, f=False):
	# use the title to classify the stuff you download
	cpath = path + '\\' + title
	# if the folder do not exist then make this folder
	if not os.path.exists(cpath):
		os.makedirs(cpath)
	# the stuff's address
	address = cpath + '\\' + find_file_name(url)
	# if the stuff exists, I suppose it had been downloaded.
	if os.path.exists(address):
		raise FileExistsError
	# if the stuff do not exist then begin to download.
	# prevent ConnectionRefusedError to convey the referer
	obj = requests.get(url, headers={'User-agent': user_agent, 'Referer': referer, 'proxies': random.sample(proxy, 1)[0]})
	# if wrong then try again
	if obj.status_code != 200:
		if not f:
			download(url, title, referer, True)
			return
		else:
			raise ConnectionError(url + ' status code: ' + str(obj.status_code))
	with open(address, 'wb') as f:
		f.write(obj.content)


def get_title(html):
	return html.xpath('//head/title/text()')[0][4:-3]


def get_img_src(html):
	return html.xpath('//div[@class="main-image"]//img/@src')[0]


def get_last_page(html):
	"""
	when there are more than one pages at this html, then I can find it.
	otherwise, it will except ValueError so I know it is only one page.
	"""
	try:
		return int(html.xpath('//div[@class="pagenavi"]//a/span/text()')[-2][8:-7])
	except ValueError:
		return 1


urls = 'http://www.mzitu.com/'


def main():
	"""
	if something is wrong, I should not crawl at start from scratch.
	Change the variable 'start' then I can begin from 'start'.
	And I try to make every page in visible status.
	"""
	start = 1
	# here is that for every group I try a different array of proxies
	for group in range(0, 500):
		i = group * 500 + 1
		while i <= group * 500 + 500:
			# make 'i' bigger than 'start'
			if start > group * 500 + 500:
				break
			while i < start:
				i += 1
			try:
				urla = urls + str(i)
				html = etree.HTML(url_to_str(urla))
				title = get_title(html)
				# if the image not found, the title should be '404 - 妹子图'
				if '404' in title:
					print('404 at ' + str(i))
					i += 1
					continue
				title = clear_dir(title)
				last_page = get_last_page(html)
				# start at page 1 and end at page 'last_page'
				for j in range(1, last_page + 1):
					urlb = urla + '/' + str(j)
					src = get_img_src(etree.HTML(url_to_str(urlb)))
					download(src, title, urlb)
				print('succeed at ' + str(i))
			# the next 3 types of errors can ignore and it does not matter
			# although I want to handle it :)
			except FileExistsError:
				print('FileExistsError at ' + str(i))
			except AttributeError:
				print('AttributeError at ' + str(i))
			except IndexError:
				print('IndexError at ' + str(i))
			except Exception as e:
				print('Error at ' + str(i))
				raise e
			i += 1
		global proxy
		proxy = get_proxy(random.sample(proxy, 1)[0])


begin = clock()
main()
print(clock() - begin)
