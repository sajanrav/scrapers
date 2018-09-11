'''
    Script to get data from FiT Generation data
    from Renewable Energy Foundation website
    ( http://www.ref.org.uk/fits/index.php )

    Usage: python get_red_fit_data.py <Output Directory> <Output CSV file> <Page Limit>
    Help : python get_red_fit_data.py -h

'''

from lxml import html
import urllib
import urllib.request
import time
import argparse as ag
import os

def request_response(url, headers):
    req = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(req)
    resp_tree = html.fromstring(response.read())
    return resp_tree

def init_out_file(f_out):
    headers = ['\"FIT ID\"','\"No.\"', '\"Post Code\"', '\"Technology\"', '\"Installation\"', '\"kW\"', '\"Commission\"', '\"Export\"', '\"Tariff\"', '\"Country\"', '\"GO Region\"', '\"Local Authority\"', '\"Related ID\"', '\"Generator Name\"']
    f_out.write(",".join(headers))
    f_out.write("\n")

def write_to_file(values, f_out):
    for ind in range(0, len(values), 14):
        val = "\"" + values[ind] + "\",\"" \
              + values[ind+1] + "\",\"" \
              + values[ind+2] + "\",\"" \
              + values[ind+3] + "\",\"" \
              + values[ind+4] + "\",\"" \
              + values[ind+5] + "\",\"" \
              + values[ind+6] + "\",\"" \
              + values[ind+7] + "\",\"" \
              + values[ind+8] + "\",\"" \
              + values[ind+9] + "\",\"" \
              + values[ind+10] + "\",\"" \
              + values[ind+11] + "\",\"" \
              + values[ind+12] + "\",\"" \
              + values[ind+13] + "\""

        f_out.write(val)
        f_out.write("\n")


if __name__ == '__main__':
    parser = ag.ArgumentParser()
    parser.add_argument('dir', help="Output Directory", type=str)
    parser.add_argument('filename', help="Name of output CSV file", type=str)
    parser.add_argument('pagelimit', help="No. of pages to be extracted", type=str)
    args = parser.parse_args()

    out_dir = args.dir
    out_file = args.filename
    page_limit = int(args.pagelimit)

    f_out = open(os.path.join(out_dir, out_file), 'w')
    init_out_file(f_out)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    for index in range(0, page_limit):
        val = index * 200
        url = 'http://www.ref.org.uk/fits/index.php?start=' + str(val) + '&order=ic&dir=asc'
        resp_tree = request_response(url, headers)
        values = resp_tree.xpath('//table[contains(@class,"data-table")]/tbody/tr//text()')
        values = [ val.replace('\n','').replace('\t','').replace('\r','') for val in values ]
        values = [ val for val in values if val != '' ]
        write_to_file(values, f_out)
        time.sleep(5)

    f_out.close()
