import multiprocessing
import requests
import urllib.request

from bs4 import BeautifulSoup
from tqdm import tqdm


year2url = {
    2014 : 'https://iclr.cc/archive/2014/conference-proceedings/',
    2015 : 'https://iclr.cc/archive/www/doku.php%3Fid=iclr2015:accepted-main.html',
    2016 : 'https://iclr.cc/archive/www/doku.php%3Fid=iclr2016:accepted-main.html',
    2018 : 'https://iclr.cc/Conferences/2018/Schedule?type=Poster',
    2019 : 'https://iclr.cc/Conferences/2019/Schedule?type=Poster',
    }


paper_dir = './paper/'


def download_url(info):
    title, paper_url = info
    urllib.request.urlretrieve(paper_url, title)

def download(year):
    # Step 1: Get urls of the paper and save it on dictionary
    title2url = {}
    url = year2url[year]
    page = requests.get(url)
    
    if year > 2017:
        baseurl = 'https://openreview.net'
        title = None
        for line in page.iter_lines():
            line = line.decode('utf-8')
            line = line.strip()
            if line.startswith('<div class="maincardBody">'):
                title = ''
                for letter in line.split('>')[1][:-5]:
                    if letter in ['\\', '/', ''':''', '*', '?', '"', '<', '>', '|']:
                        title += '_'
                    else:
                        title += letter
                title = paper_dir + '[{}][ICLR] '.format(year) + title + '.pdf'
            elif line.startswith('<a href="https://openreview.net/'):
                page_url = line.split('"')[1]
                paper_page = requests.get(page_url)
                paper_html = paper_page.text
                soup = BeautifulSoup(paper_html, 'html.parser')
                paper_url = baseurl + str(soup.select('div > h2 > a')).split('"')[3]
                title2url[title] = paper_url
                
    elif year in [2015, 2016]:
        for line in page.iter_lines():
            line = line.decode('utf-8')
            line = line.strip()
            if line.startswith('<li class="level1"><div class="li"> <a href="http://arxiv.org'):
                title = ''
                for letter in line.split('"')[14][1:-9].split('<')[0].strip():
                    if letter in ['\\', '/', ''':''', '*', '?', '"', '<', '>', '|']:
                        title += '_'
                    else:
                        title += letter
                title = paper_dir + '[{}][ICLR] '.format(year) + title + '.pdf'
                page_url = line.split('"')[5]
                paper_url = page_url.replace('abs', 'pdf')
                title2url[title] = paper_url
                
    elif year == 2014:
        paper_url = None
        for line in page.iter_lines():
            line = line.decode('utf-8')
            line = line.strip()
            if '<table xmlns=' == line.split('"')[0]:
                for sentence in line.split('"'):
                    if sentence.endswith('</p><p dir=') or sentence.endswith('</a></b></span><div><i style='):
                        temp_title = sentence.split('<')[0][1:]
                        if temp_title and paper_url:
                            title = ''
                            for letter in temp_title.strip():
                                if letter in ['\\', '/', ''':''', '*', '?', '"', '<', '>', '|']:
                                    title += '_'
                                else:
                                    title += letter
                            title = paper_dir + '[{}][ICLR] '.format(year) + title + '.pdf'
                            title2url[title] = paper_url
                            paper_url = None
                    elif sentence.startswith('http://arxiv.org'):
                        paper_url = sentence.replace('abs', 'pdf')

    # Step 2: Download paper on paper dir
    pool = multiprocessing.Pool(processes=4)
    total = len(title2url)
    with tqdm(total=total) as pbar:
        for _ in tqdm(pool.imap_unordered(download_url, list(title2url.items()))):
            pbar.update()
    pool.close()
    pool.join()