import csv
import requests
from time import clock
from lxml import etree
from bs4 import BeautifulSoup
rank = []
who = []
times = []
rating = []


def url_to_str(url):
	html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
	soup = BeautifulSoup(html.text, 'lxml')
	return soup.prettify()


def str_to_htm(s):
	return etree.HTML(s)


def url_to_htm(url):
	return str_to_htm(url_to_str(url))


def get_last_page(html):
	result = html.xpath('//div[@class="pagination"]//span[@class="page-index"]/@pageindex')
	return result[-1]


def get_other(html):
	result = html.xpath('//div[@style="background-color: white;margin:0.3em 3px 0 3px;position:relative;"]//tr/td[not(@style="text-align:left;padding-left:1em;")]/text()')
	for i, j in enumerate(result):
		cur = i % 3
		app = j[11:-10]
		if cur == 0:
			rank.append(app)
		elif cur == 1:
			times.append(app)
		else:
			rating.append(app)


def get_who(html):
	result = html.xpath('//div[@style="background-color: white;margin:0.3em 3px 0 3px;position:relative;"]//tr/td/a/@href')
	for i in result:
		who.append(i[9:])


def main():
	furl = 'http://codeforces.com/ratings'
	last_page = get_last_page(url_to_htm(furl))
	furl += '/page/'
	for i in range(1, int(last_page) + 1):
		url = furl + str(i)
		html = url_to_htm(url)
		get_who(html)
		get_other(html)
		print(i)
	with open('2018-08-26.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['rank', 'who', 'times', 'rating'])
		for j in range(len(rank)):
			writer.writerow([rank[j], who[j], times[j], rating[j]])


begin = clock()
main()
print(str(clock() - begin) + 'seconds')
# crawl at 2018-08-26 17:03
# time: 459.2107370582218 seconds
