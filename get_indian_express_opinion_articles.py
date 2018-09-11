'''
    Script to scrape opinion articles from Indian Express
    news website ( www.indianexpress.com/opinion )

    Usage : python get_indian_express_opinion_articles.py <Output Directory> <Output File> <Page Limit [Default=All]>
    Help  : python get_indian_express_opinion_articles.py -h
'''

import urllib
import urllib.request
from lxml import html
import os
import datetime
import time
import csv
import argparse as ag

def extract_article_from_link(url, headers):
    resp_tree = request_response(url, headers)
    headline = resp_tree.xpath('//h1[@itemprop="headline"]/text()')[0]
    description = resp_tree.xpath('//h2[@itemprop="description"]/text()')[0]

    article_details = resp_tree.xpath('//div[@class="editor"]//text()')
    to_ignore = resp_tree.xpath('//div[@class="editor"]/script/text()')
    article_details = [ val.replace("\n","").replace("\t","").replace(" | ","") for val in article_details if val not in to_ignore ]
    article_details = [ val for val in article_details if val != '' ]

    try:
        author = article_details[1]
        date_written = article_details[-1].replace("Updated:","").replace("Published:","").strip()
    except:
        author = "n/a"
        date_written = "n/a"

    text = resp_tree.xpath('//div[@itemprop="articleBody"]/p/text()')
    news_text = ""
    for t in text:
        news_text = news_text + t.replace("\"","").replace("\n","") + " "

    news_text = news_text[:-1]
    full_text = "\"" + date_written + "\"" + "," + "\"" + headline + "\"" + "," + "\"" + description + "\"" + "," + "\"" + author + "\"" + "," + "\"" + news_text + "\""

    return full_text
    
def get_news_article_links(links, headers):
    batch_text = []
    for link in links:
        full_text = extract_article_from_link(link, headers)
        batch_text.append(full_text)
        time.sleep(7)
        
    return batch_text

def write_to_file(article_text, f_out):
    for text in article_text:
        e_text = text.encode("utf-8")
        f_out.write(e_text)
        f_out.write("\n".encode())

def request_response(url, headers):
    req = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(req)
    resp_tree = html.fromstring(response.read())    
    return resp_tree

def get_max_sum_page(url, headers):
    elem_char = ['\n\t', '\n', '…', '\n', '»']
    resp_tree = request_response(url, headers)
    max_pages = resp_tree.xpath('//div[@class="pagination"]//text()')
    max_pages = [ val for val in max_pages if val not in elem_char ]  
    return int(max_pages[-1].replace(',',''))

def get_links_on_summary_page(url, headers):
    resp_tree = request_response(url, headers)
    news_links = resp_tree.xpath('//h6/a/@href')
    return news_links

if __name__ == '__main__':
    parser = ag.ArgumentParser()
    parser.add_argument('dir', help='Output Directory', type=str)
    parser.add_argument('filename', help='Name of output CSV file', type=str)
    parser.add_argument('--pagelimit', help='Page value limit [Default=all]', type=str)
    args = parser.parse_args()
    out_dir = args.dir
    out_file = args.filename

    f_out = open(os.path.join(out_dir, out_file),'wb')
    file_headers = ['Date-Time', 'Headline', 'Description', 'Author', 'News Text']
    header_text = ",".join(file_headers)
    f_out.write(header_text.encode())
    f_out.write("\n".encode())
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    base_url = 'https://indianexpress.com/section/opinion'
    
    if args.pagelimit is None:
        page_limit = get_max_sum_page(base_url, headers)
    else:
        page_limit = int(args.pagelimit)
    
    for page in range(1, page_limit+1):
        url = 'https://indianexpress.com/section/opinion/page/' + str(page) + '/'
        print(url)
        links = get_links_on_summary_page(url, headers)
        article_text = get_news_article_links(links, headers)
        write_to_file(article_text, f_out)
        time.sleep(10)
