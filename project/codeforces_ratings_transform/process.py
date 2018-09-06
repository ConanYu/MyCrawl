import os
import csv

PATH = os.getcwd() + '\\codeforces_ratings_data\\'
def traversing():
	list_dirs = os.walk(PATH)
	for root, dirs, files in list_dirs:
		return files


MONTH = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def leap(x):
	if x % 400 == 0 or x % 100 != 0 and x % 4 == 0:
		return True
	return False


def next_day(s):
	y = int(s[:4])
	m = int(s[5:7])
	d = int(s[-2:])
	if leap(y) and m == 2 and d == 28:
		return str(y) + '-' + str('%02d' % m) + '-29'
	if m == 12 and d == 31:
		return str(y + 1) + '-01-01'
	if d >= MONTH[m]:
		return str(y) + '-' + str('%02d' % (m + 1)) + '-01'
	return str(y) + '-' + str('%02d' % m) + '-' + str('%02d' % (d + 1))


def dict2list(dic:dict):
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]
    return sorted(lst, key=lambda x:x[1], reverse=True)


op = []
def main():
	data = dict()
	files = traversing()
	files.sort()
	date = '2010-02-19'
	with open('data.csv', 'w', encoding='gbk', newline='') as result:
		writer = csv.writer(result)
		writer.writerow(['name', 'value', 'date'])
		for file in files:
			cur = file[:10]
			while date < cur:
				cnt = 0
				for name, rate in op:
					writer.writerow([name, rate, date])
					cnt += 1
					if cnt >= 30:
						break
				date = next_day(date)
			with open(PATH + file, 'r') as f:
				reader = csv.reader(f)
				cnt = 0
				for r in reader:
					name = r[0]
					rate = r[1]
					data[name] = rate
					cnt += 1
					if cnt >= 30:
						break
			op = dict2list(data)
			cnt = 0
			for name, rate in op:
				writer.writerow([name, rate, file[:10]])
				cnt += 1
				if cnt >= 30:
					break


main()
