import csv
import requests
from lxml import etree
from bs4 import BeautifulSoup
from time import clock
title = []
star = []
release_time = []
score = []


def url_to_str(url):
	html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
	soup = BeautifulSoup(html.text, 'lxml')
	return soup.prettify()


def get_title(html):
	lis = html.xpath('//div[@class="board-item-content"]//a/@title')
	for i in lis:
		title.append(i)


def get_star(html):
	lis = html.xpath('//div[@class="board-item-content"]//p[@class="star"]/text()')
	for i in lis:
		star.append(i[16:-12])


def get_release_time(html):
	lis = html.xpath('//div[@class="board-item-content"]//p[@class="releasetime"]/text()')
	for i in lis:
		release_time.append(i[18:-12])


def get_score(html):
	lis1 = html.xpath('//div[@class="movie-item-number score-num"]//i[@class="integer"]/text()')
	lis2 = html.xpath('//div[@class="movie-item-number score-num"]//i[@class="fraction"]/text()')
	for i in range(len(lis1)):
		score.append(lis1[i][14:-13] + lis2[i][14:-13])


def output_csv(filename):
	with open(filename, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['电影名', '主演', '上映时间', '评分'])
		for i in range(len(title)):
			writer.writerow([title[i], star[i], release_time[i], score[i]])


def main():
	urls = 'http://maoyan.com/board/4?offset='
	# offset=range(0, 100, 10)
	for off in range(0, 100, 10):
		url = urls + str(off)
		txt = url_to_str(url)
		obj = etree.HTML(txt)
		get_title(obj)
		get_star(obj)
		get_release_time(obj)
		get_score(obj)
	output_csv('2018-08-26-maoyan.csv')


begin = clock()
main()
print(clock() - begin)
# crawl at 2018-08-26 11:42
