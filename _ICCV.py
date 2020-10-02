import multiprocessing
import requests
import urllib.request

from tqdm import tqdm


baseurl = 'https://openaccess.thecvf.com/'

year2url = {
    2013 : ['https://openaccess.thecvf.com/ICCV2013'],
    2015 : ['https://openaccess.thecvf.com/ICCV2015'],
    2017 : ['https://openaccess.thecvf.com/ICCV2017'],
    2019 : ['https://openaccess.thecvf.com/ICCV2019?day=2019-10-29',
            'https://openaccess.thecvf.com/ICCV2019?day=2019-10-30',
            'https://openaccess.thecvf.com/ICCV2019?day=2019-10-31',
            'https://openaccess.thecvf.com/ICCV2019?day=2019-11-01'],
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
                title = paper_dir + '[{}][ICCV] '.format(year) + title + '.pdf'
                title2url[title] = baseurl + page_url

    # Step 2: Download paper on paper dir
    pool = multiprocessing.Pool(processes=4)
    total = len(title2url)
    with tqdm(total=total) as pbar:
        for _ in tqdm(pool.imap_unordered(download_url, list(title2url.items()))):
            pbar.update()
    pool.close()
    pool.join()