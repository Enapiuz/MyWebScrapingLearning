__author__ = 'enapiuz'

from grab import Grab
from pymongo.errors import DuplicateKeyError
from helpers import db as dbhelper


g = Grab()
g.go("http://habrahabr.ru")
global_links = g.doc.select("//*[@class='post shortcuts_item']/h1/a[1]")

for page in global_links:
    page_link = page.attr('href')
    post_grab = Grab()
    post_grab.go(page_link)

    try:
        post_title = post_grab.doc.select("//span[@class='post_title']")[0].text()
    except IndexError as e:
        post_title = 'No Title'

    try:
        favs_count = post_grab.doc.select("//*[@class='favs_count']")[0].text()
    except IndexError as e:
        favs_count = 0

    try:
        post_score = post_grab.doc \
            .select("//div[@class='infopanel_wrapper']//div[contains(@class, 'mark')]/span[@class='score']")[0].text()
        if post_score == '—':
            post_score = 0
    except IndexError as e:
        post_score = 0

    try:
        comments_count = post_grab.doc.select("//*[@id='comments_count']")[0].text()
    except IndexError as e:
        comments_count = 0

    try:
        author = post_grab.doc.select("//div[@class='author']/a")[0].text()
    except IndexError as e:
        author = "No Author O_o"

    try:
        id = dbhelper.save_entry({
            "href": page_link,
            "title": post_title,
            "favs": favs_count,
            "score": post_score,
            "comments": comments_count,
            "author": author
        })

        print(str(id))
    except DuplicateKeyError as e:
        print("Post %s already exists" % page_link)