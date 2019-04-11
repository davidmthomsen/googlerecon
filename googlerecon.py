#!/usr/bin/python3
import argparse
import sys
import requests
import re
from bs4 import *
import time
from user_agent import generate_user_agent
from pprint import pprint


class Parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('Error: %s\n' % message)
        self.print_help()
        sys.exit(2)


parser = Parser()
parser.add_argument('domain')
args = parser.parse_args()


def google_scrape(domain):

    checks = {
        "Directory Listing": "intitle:index.of site:{}",
        "Configuration Files": "ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf | ext:cfg | ext:txt | ext:ora | ext:ini site:{}",
        "Database Files": "ext:sql | ext:dbf | ext:mdb site:{}",
        "Database Dumps": "ext:sql 'phpMyAdmin SQL Dump' site:{}",
        "Log Files": "ext:log | ext:txt site:{}",
        "Session IDs": "inurl:sid= | inurl:JSESSIONID | inurl:PHPSESSID site:{}",
        "Backup Files": "ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup site:{}",
        "Login Pages": "inurl:login site:{}",
        "JIRA and Confluence Pages": "intext:'Powered by Atlassian Confluence' | intitle:'JIRA login' site:{}",
        "SQL Error Pages": "intext:'sql syntax near' | intext:'syntax error has occured' | intext:'incorrect syntax near' | intext:'unexpected end of SQL command' | intext:'Warning: mysql_connect()'' | intext:'Warning: mysql_query()' | intext:'Warning: pg_connect()' site:{}",
        "Exposed Docs": "ext:doc | ext:docx | ext:odt | ext:pdf | ext:rtf | ext:sxw | ext:psw | ext:ppt | ext:pptx | ext:pps | ext:csv | ext:xls | ext:xlsx | ext:cvs site:{}",
        "phpinfo()": "ext:php intitle:phpinfo 'published by the PHP Group' site:{}",
        "Private Keys": "ext:key intext:'BEGIN RSA PRIVATE KEY' site:{}",
        "Source Code Repos": "inurl:.git/ | inurl:.svn/ | inurl:/uploads/ | inurl:/api/v1/  site:{}"
    }
    headers = pprint(generate_user_agent(os=('mac', 'linux')))

    try:
        for check in checks.items():
            print('[!] Checking ' + check[0])

            query = check[1].format(domain)
            url = 'https://www.google.com/search?q={}'.format(query)
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, features="html.parser")
            links = soup.find_all("h3", class_="r")

            for link in links:
                a = link.findAll('a')[0].attrs['href']
                p = re.compile(r'^\/url\?q=(.*)\&sa')
                raw_link = re.findall(p, a)[0]
                print(raw_link)

            print("")
            time.sleep(.600)
    except:
        print("Search failed")


def main(args):
    results = google_scrape(args.domain)


if __name__ == '__main__':
    main(args)
