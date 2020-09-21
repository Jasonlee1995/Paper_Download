import multiprocessing
import requests
import urllib.request

from tqdm import tqdm


baseurl = 'https://openaccess.thecvf.com/'

year2url = {
    2013 : ['https://openaccess.thecvf.com/CVPR2013'],
    2014 : ['https://openaccess.thecvf.com/CVPR2014'],
    2015 : ['https://openaccess.thecvf.com/CVPR2015'],
    2016 : ['https://openaccess.thecvf.com/CVPR2016'],
    2017 : ['https://openaccess.thecvf.com/CVPR2017'],
    2018 : ['https://openaccess.thecvf.com/CVPR2018?day=2018-06-19',
            'https://openaccess.thecvf.com/CVPR2018?day=2018-06-20',
            'https://openaccess.thecvf.com/CVPR2018?day=2018-06-21'],
    2019 : ['https://openaccess.thecvf.com/CVPR2019?day=2019-06-18',
            'https://openaccess.thecvf.com/CVPR2019?day=2019-06-19',
            'https://openaccess.thecvf.com/CVPR2019?day=2019-06-20'],
    }


paper_dir = './paper/'


def download_url(info):
    title, page_url = info
    urllib.request.urlretrieve(page_url, title)

def download(year):
    # Step 1: Get urls of the paper and save it on dictionary
    title2url = {}
    page_url = None
    for url in year2url[year]:
        page = requests.get(url)
        for line in page.iter_lines():
            line = line.decode('utf-8')
            if line.endswith('pdf</a>]'):
                page_url = line.split('"')[1]
            elif line.startswith('title'):
                title = ''
                for letter in line.split('{')[1][:-6]:
                    if letter in ['\\', '/', ''':''', '*', '?', '"', '<', '>', '|']:
                        title += '_'
                    else:
                        title += letter
                title = paper_dir + '[{}][CVPR] '.format(year) + title + '.pdf'
                title2url[title] = baseurl + page_url

    # Step 2: Download paper on paper dir
    pool = multiprocessing.Pool(processes=4)
    total = len(title2url)
    with tqdm(total=total) as pbar:
        for _ in tqdm(pool.imap_unordered(download_url, list(title2url.items()))):
            pbar.update()
    pool.close()
    pool.join()