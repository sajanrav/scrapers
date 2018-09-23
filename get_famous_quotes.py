'''
    Script to get famous quotations by various people
    from the site http://quotes.toscrape.com/

    Usage : python get_famous_quotes.py <outfile> <outdir>
    Help  : python get_famous_quotes.py -h
'''


import urllib
import urllib.request
from lxml import html
import csv
import time
import argparse as ag
import os

def request_response(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    request = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(request)
    resp_tree = html.fromstring(response.read())
    return resp_tree

def get_author_desc(author_urls):
    dates_list = []
    loc_list = []
    desc_list = []

    for auth_url in author_urls:
        resp_tree = request_response(auth_url)
        auth_born_date = resp_tree.xpath("//span[@class='author-born-date']/text()")
        auth_born_location = resp_tree.xpath("//span[@class='author-born-location']/text()")
        auth_born_location = [ val.replace("in ","") for val in auth_born_location ]
        auth_desc = resp_tree.xpath("//div[@class='author-description']/text()")
        auth_desc = [ val.strip().replace("\"","").replace(",","") for val in auth_desc ]

        dates_list.append(auth_born_date[0])
        loc_list.append(auth_born_location[0])
        desc_list.append(auth_desc[0])
        time.sleep(5)

    return dates_list, loc_list, desc_list
        
def parse_data(resp_tree):
    quote = resp_tree.xpath("//div[@class='quote']/span[@itemprop='text']/text()")
    quote = [ val.replace('“', '').replace('”','') for val in quote ]

    author_name = resp_tree.xpath("//div[@class='quote']/span/small[@itemprop='author']/text()")
    author_urls = resp_tree.xpath("//div[@class='quote']/span/a[contains(text(),'about')]/@href")
    author_urls = [ 'http://quotes.toscrape.com' + val for val in author_urls ]
    auth_born_date, auth_born_location, auth_desc = get_author_desc(author_urls)
    
    tags = resp_tree.xpath("//div[@class='quote']/div[@class='tags']/meta/@content")
    tags = [ 'n/a' if val == '' else val for val in tags ]
    return list(zip(quote, author_name, auth_born_date, auth_born_location, auth_desc, tags))

def write_to_file(f, tup):                    
    for val in tup:
        text_to_write = "\"" + val[0] + "\",\"" + val[1] + "\",\"" + val[2] + "\",\"" + val[3] + "\",\"" + val[4] + "\",\"" + "\",\"" + val[5] + "\""
        f.write(text_to_write)
        f.write("\n")

def init_out_file(out_file, out_dir):
    f = open(os.path.join(out_dir, out_file), "w", encoding='utf8')
    f_headers = ["\"Quote\"", "\"Author\"", "\"Author Born Date\"", "\"Aurhor Born Location\"", "\"Author Description\"", "\"Tags\""]
    headers = ",".join(f_headers)
    f.write(headers)
    f.write("\n")
    return f
        
if __name__ == "__main__":
    parser = ag.ArgumentParser()
    parser.add_argument('outfile', help='Output CSV file', type=str)
    parser.add_argument('outdir', help='Output directory', type=str)
    args = parser.parse_args()
    
    out_file = args.outfile
    out_dir = args.outdir
    
    base_url = "http://quotes.toscrape.com/page/"
    f = init_out_file(out_file, out_dir)

    for ind in range(1,11):
        url = base_url + str(ind) + "/"
        resp_tree = request_response(url)
        final = parse_data(resp_tree)
        write_to_file(f, final)
        time.sleep(5)

    f.close()
