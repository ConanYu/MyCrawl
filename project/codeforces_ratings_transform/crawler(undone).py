import os
import csv
import time
import random
import requests
from lxml import etree
from pxy import get_proxy
from bs4 import BeautifulSoup
proxy = get_proxy()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
URL = 'http://codeforces.com/contests'


def url_to_str(url, times=0):
	"""
	I will give ten chances to you.
	If you fail still, I..I will cry.
	"""
	if times >= 10:
		raise ConnectionError(url)
	global proxy
	try:
		html = requests.get(url, headers={'User-agent': user_agent, 'proxies': random.sample(proxy, 1)[0]})
		if html.status_code != 200:
			raise ConnectionError(url)
		return html.text
	except Exception:
		time.sleep(1)
		proxy = get_proxy(random.sample(proxy, 1)[0])
		return url_to_str(url, times + 1)


def url_to_soup(url):
	return BeautifulSoup(url_to_str(url), 'lxml')


def url_to_etree(url):
	return etree.HTML(url_to_soup(url).prettify())


def get_last_page():
	obj = url_to_etree(URL)
	s = obj.xpath('//div[@class="pagination"]//span[@class="page-index"]//a/@href')[-1]
	pos = 0
	for i, j in enumerate(s):
		if j == '/':
			pos = i + 1
	return int(s[pos:])


def direct(url):
	if url[0] == '/' and url[1] != '/':
		return 'codeforces.com' + url
	return url


def clear_space(s):
	ret = ''
	for i in s:
		if i != ' ' and i != '\n':
			ret += i
	return ret


def del_all(soup, att, value):
	[i.extract() for i in soup.find_all(name='td' ,attr={att, value})]
	return soup


def get_idx(html):
	return html.xpath('//div[@class="contests-table"]//div[@class="datatable"]//tr/@data-contestid')


en_to_num = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
             'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
def get_time(html):
	ret = []
	arr = html.xpath('//div[@class="contests-table"]//div[@class="datatable"]//span[@class="format-date"]/text()')
	for i in arr:
		txt = i[14:-13]
		ret.append(txt[7:11] + '-' + en_to_num[txt[:3]] + '-' + txt[4:6] + '                    ' + txt[12:14] + txt[15:])
	return ret


def get_lpg(html):
	# last page of ratings
	try:
		s = html.xpath('//div[@class="custom-links-pagination"]//nobr//a/@href')[-1]
	except IndexError:
		return 1
	pos = 0
	for i, j in enumerate(s):
		if j == '/':
			pos = i + 1
	return int(s[pos:])


def get_change_rate(html):
	ret = []
	arr = html.xpath('//span[@style="font-weight:bold;"]/text()')
	for i, j in enumerate(arr):
		if i & 1:
			ret.append(clear_space(j))
	return ret


def get_change_who(html):
	ret = []
	arr = html.xpath('//a[contains(@href,"/profile/")]/@href')
	for i in arr:
		ret.append(i[9:])
	return ret


def check(html):
	return 'Standings' in html.xpath('//head/title/text()')[0]


path = os.getcwd() + '\\codeforces_ratings_data\\'
# prevent unrated contest
st = set(['1017', '874'])
# st = {'1017', '874'}
def main():
	cnt = 0
	contestid = get_last_page()
	for i in range(1, contestid + 1):
		furl = URL + '/page/' + str(i)
		html = url_to_etree(furl)
		idx = get_idx(html)
		tim = get_time(html)
		for j in range(len(idx)):
			cnt += 1
			address = path + tim[j] + str(cnt % 10) + '.csv'
			if idx[j] in st or os.path.exists(address):
				continue
			surl = 'http://codeforces.com/contest/' + idx[j] + '/ratings'
			html = url_to_etree(surl)
			# prevent unrated contest
			if check(html):
				continue
			print(idx[j] + ':')
			lpg = get_lpg(html)
			who = []
			rate = []
			for k in range(1, lpg + 1):
				turl = 'http://codeforces.com/contest/' + str(idx[j]) + '/ratings/page/' + str(k)
				html = url_to_etree(turl)
				who += get_change_who(html)
				rate += get_change_rate(html)
				print(k)
			with open(address, 'w', encoding='gbk', newline='') as csvfile:
				writer = csv.writer(csvfile)
				for k in range(len(who)):
					writer.writerow([who[k], rate[k]])
			print(address + ' has done!')


main()
