import requests
from lxml import etree

def getlist_organization(idx):
    url = 'http://codeforces.com/ratings/organization/' + str(idx)
    response = requests.get(url)
    html = etree.HTML(response.text)
    result = html.xpath('//div[@class="datatable ratingsDatatable"]//a/@href')
    return [e[9:] for e in result]

if __name__ == '__main__':
    print(getlist_organization(750))

