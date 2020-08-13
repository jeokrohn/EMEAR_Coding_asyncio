#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin
import time
import threading
import concurrent.futures
import asyncio
import aiohttp

log = logging.getLogger(__name__)

FN_BASE_PAGE = 'https://www.cisco.com/c/en/us/support/web/tsd-products-field-notice-summary.html'


def get_field_notice_urls():
    """
    Access page with Cisco fields notices and extract all URLs of recent field notices
    :return: list of fields notice URLs
    """
    page = get_page(url=FN_BASE_PAGE)
    log.info('Cooking soup')
    soup = BeautifulSoup(markup=page, features='lxml')
    """
    This is what the field notice entries look like
    <ul class="doc-sublist">
            <li><a href="/c/en/us/support/docs/field-notices/632/fn63208.html"><span 
            class='most_recent_link_title'>Contact Center:Field Notice: FN - 63208 - Cisco Interaction Manager 4.2(5) 
            upgrade fails due to SQL Collation incompatibility - Software Upgrade Recommended</span></a>
<span class="most_recent_link_date">Updated&nbsp;30-Jun-2020</span><br /></li>
    """

    # find all <li> with a span of class 'most_recent_link_title>'
    def li_with_most_recent_link_title_span(tag):
        return tag.name == 'li' and (span := tag.span) and span.attrs.get('class', [''])[0] == 'most_recent_link_title'

    log.info('Finding all field notice links')
    li = soup.find_all(li_with_most_recent_link_title_span)
    log.info(f'found {len(li)} field notices')

    # determine full urls from href values
    urls = [urljoin(FN_BASE_PAGE, l.a['href']) for l in li]
    return urls


def get_page(url):
    """
    GET the page via given URL and return markuo
    :param url: URL to access
    :return: markup of retrieved web page
    """
    with requests.Session() as session:
        r = session.get(url=url)
        r.raise_for_status()
    return r.text


def get_field_notices_futures(urls):
    """
    Retrieve all field notices using ThreadPoolExecutor and retrieve results using as_completed()
    :param urls:  list of field notice URLs
    :return: None
    """
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_map = {executor.submit(get_page, url): i for i, url in enumerate(urls)}
        for completed_future in concurrent.futures.as_completed(future_map):
            i = future_map[completed_future]
            r = completed_future.result()
    log.info(f'Futures thread: got {len(urls)} field notices in {(time.perf_counter() - start) * 1000:.3f}ms')


async def get_page_async(session, sem, url):
    """
    GET the page via given URL and return markuo
    :param url: URL to access
    :return: markup of retrieved web page
    """

    async with sem:
        async with session.get(url) as r:
            r.raise_for_status()
            text = await r.text()
    return text


async def get_field_notices_asyncio(urls):
    sem = asyncio.Semaphore(50)
    async with aiohttp.ClientSession() as session:
        start = time.perf_counter()
        tasks = [get_page_async(session, sem, url) for url in urls]
        await asyncio.gather(*tasks, return_exceptions=False)
        log.info(f'Asyncio: got {len(urls)} field notices in {(time.perf_counter() - start) * 1000:.3f}ms')


if __name__ == '__main__':
    f = logging.Formatter('%(asctime)s [%(levelname)s] [%(threadName)s] %(name)s: %(message)s')
    h = logging.StreamHandler()
    h.setFormatter(f)
    log.addHandler(h)
    log.setLevel(logging.INFO)

    urls = get_field_notice_urls()

    for i in [5, 10, 20, 50, 100]:
        log.info('=' * 100)
        get_field_notices_futures(urls * i)

        log.info('=' * 100)
        asyncio.run(get_field_notices_asyncio(urls * i))
