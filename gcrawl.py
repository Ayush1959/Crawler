from lxml import html
import requests
import time

class AppCrawler:

    def __init__(self, starting_url, depth):
        self.starting_url = starting_url
        self.depth = depth
        self.current_depth = 0
        self.depth_links = []
        self.apps = []

    def crawl(self):
        app = self.get_app_from_link(self.starting_url)
        self.apps.append(app)
        self.depth_links.append(app.links)


        while self.current_depth < self.depth:
            current_links = []
            for link in self.depth_links[self.current_depth]:
                current_app = self.get_app_from_link(link)
                current_links.extend(current_app.links)
                self.apps.append(current_app)
                time.sleep(5)
            self.current_depth += 1
            self.depth_links.append(current_links)



    def get_app_from_link(self, link):
        start_page = requests.get(link)
        tree = html.fromstring(start_page.text)

        name = tree.xpath('//h1[@itemprop="name"]/span/text()')[0]
        developer = tree.xpath('//div[@class="i4sPve"]//*/a[@class="hrTbp R8zArc"]/text()')[0]
        type = tree.xpath('//a[@itemprop="genre"]/text()')[0]
        rating = tree.xpath('//div[@class="BHMmbe"]/text()')[0]
        new_links = tree.xpath('//div[@class="wXUyZd"]/a/@href')
        links = ["https://play.google.com" + x for x in new_links]
        app = App(name, developer, type, rating, links)
        return app


class App:

    def __init__(self, name, developer, type, rating, links):
        self.name = name
        self.developer = developer
        self.type = type
        self.rating = rating
        self.links = links

    def __str__(self):
        return("Name: " + self.name +
        "\r\nDeveloper: " + self.developer +
        "\r\nType: " + self.type +
        "\r\nRating: " + self.rating + "\n")


crawler = AppCrawler('https://play.google.com/store/apps/details?id=com.tencent.ig&hl=en_IN', 1)
crawler.crawl()

for app in crawler.apps:
    print (app)
