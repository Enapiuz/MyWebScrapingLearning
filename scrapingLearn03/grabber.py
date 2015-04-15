__author__ = 'enapiuz'

import sys
import argparse
import urllib.parse
from grab.spider import Spider, Task
from selection import XpathSelector
from helpers import db


class GoogleParser(Spider):
    def __init__(self, param_pages_limit, param_query):
        self.param_pages_limit = param_pages_limit
        self.param_query = param_query
        super().__init__()

    def task_generator(self):
        yield Task('do_request', url="https://www.google.com/?" + urllib.parse.urlencode({'q': self.param_query}))

    def task_do_request(self, grab, task):
        print(task.url)


if __name__ == '__main__':
    # получаем поисковой запрос и количество просматриваемых страниц
    argParser = argparse.ArgumentParser()
    argParser.add_argument('-q', '--query')
    argParser.add_argument('-p', '--pages')
    args = argParser.parse_args()
    query = args.query or ""
    pages_limit = args.pages or 1
    
    if len(query) == 0:
        sys.exit('Usage: (-q "query") [-p total_pages]')

    parser = GoogleParser(pages_limit, query)
    parser.run()
