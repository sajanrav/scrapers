'''
    Script to extract facebook, linkedin and twitter
    links from a web page and print on console

    Usage : python get_social_media_links_from_page.py <url>
    Help  : python get_social_media_links_from_page.py -h
    
'''

import urllib.request
from lxml import html
import re
import argparse


def request_response(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    request = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(request)
    resp_tree = html.fromstring(response.read())
    return resp_tree


def get_links(url):
    sites = ['facebook.com', 'linkedin.com', 'twitter.com']
    sm_links = {}
    resp_tree = request_response(url)
    links = resp_tree.xpath("//a//@href")

    for val in links:
        for site in sites:
            regex = "[\d|\D]+" + re.escape(site) + "[\d|\D]+"
            if re.search(regex, val):
                sm_links[site.replace(".com","")] = val
    
    return sm_links


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='URL', type=str)
    args = parser.parse_args()

    url = args.url
    sm_links = get_links(url)
    print(sm_links)
