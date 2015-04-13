__author__ = 'enapiuz'

from grab.spider import Spider, Task
from selection import XpathSelector
from helpers import mongo as db


class MegaParser(Spider):
    max_page = 100
    processed = 0

    def task_generator(self):
        for page_num in range(self.max_page):
            yield Task('page', url='http://habrahabr.ru/all/page{number}'.format(number=page_num + 1))

            self.processed += 1
            print("Processed {count}%".format(count=round((self.processed/self.max_page)*100)))

    def task_page(self, grab, task):
        cp = grab.doc.select('//*[@id="nav-pages"]/li/em').text()
        for article_url in grab.doc.select("//h1[@class='title']/a[@class='post_title']/@href"):
            yield Task('article', url=article_url.text(), current_page=cp)

    def task_article(self, grab, task):
        page_header = grab.doc.select("//span[@class='post_title']").one(default=XpathSelector('No Header!')).text()
        page_favs = grab.doc.select("//*[@class='favs_count']").one(default=XpathSelector('0')).text()
        page_score = grab.doc.\
            select("//div[@class='infopanel_wrapper']//div[contains(@class, 'mark')]/span[@class='score']").\
            one(default=XpathSelector('0')).text()
        page_comments_count = grab.doc.select("//*[@id='comments_count']").one(default=XpathSelector('0')).text()
        page_author = grab.doc.select("//div[@class='author']/a").one(default=XpathSelector('No Author!')).text()
        page_date = grab.doc.select("//div[@class='published']").one(default=XpathSelector('0')).text()

        self.save_result(data={
            'page': task.current_page,
            'url': task.url,
            'header': page_header,
            'author': page_author,
            'favorites': page_favs,
            'score': page_score,
            'comments': page_comments_count,
            'date': page_date
        })

    # а нужен ли тут статический метод?
    @staticmethod
    def save_result(data):
        db.save_entry(data)


if __name__ == '__main__':
    parser = MegaParser()
    parser.run()