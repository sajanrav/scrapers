'''
    Script to fetch statistics data of a particular year
    from College Football Analytics website ( www.cfbanalytics.com )

    Usage : python get_cfbanalytics_data.com <year> <statistics> <outputfile> <output directory>
    Help  : python get_cfbanalytics_data.com -h
'''

from lxml import html
import os
import urllib.request
import argparse as ag
import csv

INSTANCE = 'lOcN472d6DMnq6dGyrufa-vu8-iPhiO3pZJoitj9Jpo.eyJpbnN0YW5jZUlkIjoiMTk4ZmMxOWQtYTYxZi00ZDFkLTk3NDEtOGY2N2YxZTQ0ZmI3IiwiYXBwRGVmSWQiOiIxMzQxMzlmMy1mMmEwLTJjMmMtNjkzYy1lZDIyMTY1Y2ZkODQiLCJtZXRhU2l0ZUlkIjoiODE1ZjI1YTgtNjEwZC00ZDZkLTljNjUtODU1YzE4ZjA3N2YyIiwic2lnbkRhdGUiOiIyMDE4LTA5LTE4VDA3OjUwOjQxLjE1NFoiLCJ1aWQiOm51bGwsImlwQW5kUG9ydCI6IjEwMy4yMTUuNTQuOTMvMTkyMTIiLCJ2ZW5kb3JQcm9kdWN0SWQiOm51bGwsImRlbW9Nb2RlIjpmYWxzZSwiYWlkIjoiMDI1NDBlM2QtYTAxZC00MjMyLTkyZjctZGU4YTQwMjcyYTM5IiwiYmlUb2tlbiI6Ijk4ZDBlNDM1LWM3MTItMDA3MC0wYjI0LTBhM2JlOTE0Mzg0NSIsInNpdGVPd25lcklkIjoiMDJiNTM3YTEtYTk5MC00ODYyLThjMWItNWNhYzgxZDAzZjVhIn0'

class scraper:
    def __init__(self, year, stat, out_file, out_dir, url_data):
        self.year = year
        self.stat = stat
        self.out_dir = out_dir
        self.out_file = out_file
        self.full_path = os.path.join(out_dir, out_file)
        self.url_data = url_data

    def initialize_urls(self):
        url_dict = {}
        with open(self.url_data, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                url = 'https://wix-visual-data.appspot.com/app/file?compId=' + row[2] + '&instance=' + INSTANCE
                key = (row[0], row[1])
                url_dict[key] = url
                
        self.url_dict = url_dict
        f.close()

    def request_response(self):
        key = (self.stat, self.year)
        url = self.url_dict[key]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        self.response = response.read().decode()
        
    def parse_text(self):
        self.data = self.response.split('\r\n')
        
    def write_to_file(self):
        with open(self.full_path, 'w') as f:
            for val in self.data:
                f.write('%s\n' % val)

        f.close()
                
if __name__ == "__main__":
    parser = ag.ArgumentParser()
    parser.add_argument('year', help='year', type=str)
    parser.add_argument('stat', help='type of stat (ratings | field-position | passing | rushing)', type=str)
    parser.add_argument('outputfile', help='output file', type=str)
    parser.add_argument('outputdir', help='output directory', type=str)
    parser.add_argument('urldata', help='full path with file name of master file of all URLs', type=str)
    args = parser.parse_args()

    year = args.year
    stat = args.stat
    out_file = args.outputfile
    out_dir = args.outputdir
    url_data = args.urldata

    scraper_obj = scraper(year, stat, out_file, out_dir, url_data)
    scraper_obj.initialize_urls()
    scraper_obj.request_response()
    scraper_obj.parse_text()
    scraper_obj.write_to_file()
