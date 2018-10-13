import requests
from lxml import etree

def getlist_organization(idx):
    url = 'http://codeforces.com/ratings/organization/' + str(idx)
    response = requests.get(url)
    html = etree.HTML(response.text)
    result = html.xpath('//*[@class="datatable ratingsDatatable"]//a/@href')
    v = [e[9:] for e in result]
    return v

if __name__ == '__main__':
    print(getlist_organization(750))

