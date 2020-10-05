import multiprocessing
import requests
import urllib.request

from tqdm import tqdm


baseurl = 'https://openaccess.thecvf.com/'

year2url = {
    2013 : 'http://proceedings.mlr.press/v28/',
    2014 : 'http://proceedings.mlr.press/v32/',
    2015 : 'http://proceedings.mlr.press/v37/',
    2016 : 'http://proceedings.mlr.press/v48/',
    2017 : 'http://proceedings.mlr.press/v70/',
    2018 : 'http://proceedings.mlr.press/v80/',
    2019 : 'http://proceedings.mlr.press/v97/',
    }


paper_dir = './paper/'


def download_url(info):
    title, paper_url = info
    urllib.request.urlretrieve(paper_url, title)

def download(year):
    # Step 1: Get urls of the paper and save it on dictionary
    title2url = {}
    title = None
    url = year2url[year]
    page = requests.get(url)
    for line in page.iter_lines():
        line = line.decode('utf-8')
        line = line.strip()
        if line.startswith('<p class="title">'):
            title = ''
            for letter in line.split('>')[1][:-3]:
                if letter in ['\\', '/', ''':''', '*', '?', '"', '<', '>', '|']:
                    title += '_'
                else:
                    title += letter
            title = paper_dir + '[{}][ICML] '.format(year) + title + '.pdf'
        elif line.startswith('[<a href') and ('Download' in line):
            paper_url = line.split(',')[4].strip()
            title2url[title] = paper_url

    # Step 2: Download paper on paper dir
    pool = multiprocessing.Pool(processes=4)
    total = len(title2url)
    with tqdm(total=total) as pbar:
        for _ in tqdm(pool.imap_unordered(download_url, list(title2url.items()))):
            pbar.update()
    pool.close()
    pool.join()