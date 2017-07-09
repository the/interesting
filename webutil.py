#!/usr/bin/env python3
import sys, os, logging, urllib.request, bs4, urllib.parse

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

logger = logging.getLogger(__name__)

def get_page_titles(urls):
    return [get_page_title(url) for url in urls]

def get_page_title(url):
    page = get_page(url)
    if page:
        title = find_meta_title(page)
        if title and len(title) > 0:
            return title

        titles = [find_page_title(page)]
        titles.extend(find_document_titles(page))
        titles = list(reversed(sorted(filter(None, titles), key=len)))
        if len(titles) > 0:
            return titles[0]

    return ''

def get_page(url):
    try:
        data = None
        path = path_for_url(url)
        if os.path.isfile(path):
            with open(path, 'r') as file:
                data = file.read()
        else:
            data = get_url_data(url)

        page = bs4.BeautifulSoup(data, 'html.parser')
        return page
    except Exception as err:
        logger.warning('Could not load page for {}: {}'.format(url, err))
        return None

def save_page(url):
    data = get_url_data(url)
    with open(path_for_url(url), 'wb') as file:
        file.write(data)

def get_url_data(url):
    request = urllib.request.Request(url, data=None, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(request) as response:
        return response.read()

def path_for_url(url):
    filename = urllib.parse.quote_plus(url)
    return os.path.join('webpages', filename)

def find_meta_title(page):
    title = None

    meta_title = page.find('meta',  property='og:title') 
    if meta_title:
        title = meta_title['content']

    logger.debug('meta.title={}'.format(title))
    return title

def find_page_title(page):
    if page.title:
        title = page.title.string
        logger.debug('page.title={}'.format(title))
        return title

def find_document_titles(page):
    def append_texts_from_tags(tag, titles):
        for element in page.findAll(tag):
            title = element.get_text()
            logger.debug('{}={}'.format(element.name, title))
            titles.append(title)

    titles = []
    append_texts_from_tags('h1', titles)
    return titles

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) == 2:
        print(get_page_title(sys.argv[1]))
    else:
        print('usage: webutil.py url')
