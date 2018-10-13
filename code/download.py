import os
import requests

def find_file_name(url):
    def clear_dir(obj):
        st = set(r'?*/\<>:"|')
        ret = ''
        for i in obj:
            if i not in st:
                ret += i
        return ret

    pos = 0
    for i, j in enumerate(url):
        if j == '/':
            pos = i
    return clear_dir(url[pos:])

def download(url, path, **header):
    if header.get('User-agent', None) is None:
        header['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    if not os.path.exists(path):
        os.makedirs(path)
    address = path + '\\' + find_file_name(url)
    if os.path.exists(address):
        raise FileExistsError
    obj = requests.get(url, headers=header)
    if obj.status_code != 200:
        raise ConnectionError('status_code is not 200.')
    with open(address, 'wb') as f:
        f.write(obj.content)
