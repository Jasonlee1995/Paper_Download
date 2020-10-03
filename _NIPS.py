import multiprocessing
import requests
import urllib.request

from tqdm import tqdm


baseurl = 'https://papers.nips.cc/'

year2url = {
    1987 : 'https://papers.nips.cc/book/neural-information-processing-systems-1987',
    1988 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-1-1988',
    1989 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-2-1989',
    1990 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-3-1990',
    1991 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-4-1991',
    1992 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-5-1992',
    1993 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-6-1993',
    1994 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-7-1994',
    1995 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-8-1995',
    1996 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-9-1996',
    1997 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-10-1997',
    1998 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-11-1998',
    1999 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-12-1999',
    2000 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-13-2000',
    2001 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-14-2001',
    2002 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-15-2002',
    2003 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-16-2003',
    2004 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-17-2004',
    2005 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-18-2005',
    2006 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-19-2006',
    2007 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-20-2007',
    2008 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-21-2008',
    2009 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-22-2009',
    2010 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-23-2010',
    2011 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-24-2011',
    2012 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-25-2012',
    2013 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-26-2013',
    2014 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-27-2014',
    2015 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-28-2015',
    2016 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-29-2016',
    2017 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-30-2017',
    2018 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-31-2018',
    2019 : 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-32-2019',
    }


paper_dir = './paper/'


def download_url(info):
    title, page_url = info
    try:
        urllib.request.urlretrieve(page_url, title)
    except:
        print('Error on paper name {} with url {}'.format(title, page_url))
    

def download(year):
    # Step 1: Get urls of the paper and save it on dictionary
    title2url = {}
    url = year2url[year]
    page = requests.get(url)
    for line in page.iter_lines():
        line = line.decode('utf-8')
        line = line.strip()
        if line.startswith('<li><a href="/paper'):
            title = ''
            for letter in line.split('>')[2][:-3]:
                if letter in ['\\', '/', ''':''', '*', '?', '"', '<', '>', '|']:
                    title += '_'
                else:
                    title += letter
            title = paper_dir + '[{}][NIPS] '.format(year) + title + '.pdf'
            paper_url = baseurl + line.split('>')[1][9:-1]
            paper_page = requests.get(paper_url)
            for paper_line in paper_page.iter_lines():
                paper_line = paper_line.decode('utf-8')
                paper_line = paper_line.strip()
                if paper_line.endswith('[PDF]</a>'):
                    title2url[title] = baseurl + paper_line.split('"')[1]
                    break

    # Step 2: Download paper on paper dir
    pool = multiprocessing.Pool(processes=4)
    total = len(title2url)
    with tqdm(total=total) as pbar:
        for _ in tqdm(pool.imap_unordered(download_url, list(title2url.items()))):
            pbar.update()
    pool.close()
    pool.join()