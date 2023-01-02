import json
import re
import scrapy

from scrapy import signals
from scrapy.signalmanager import dispatcher
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapper.db import Database

class RealEstateSpider(scrapy.Spider):
    name = "scrap_reality"
    base_url = "https://www.sreality.cz"
    flat_detail_url = f"{base_url}/detail/prodej/byt"
    start_urls = [f"{base_url}/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&page=0&per_page=500"]

    def parse(self, response, **kwargs):
        response_json = json.loads(response.body)
        for flat in response_json.get('_embedded').get('estates'):
            title = re.sub(r'\s', ' ', flat.get('name'))
            image_url = flat.get('_links').get('images')[0].get('href')

            locality = flat['seo']['locality'] 
            flat_type = title.split(" ")[2]
            flat_number = flat["_links"]['self']['href'].split("/")[-1]
            url = f"{self.flat_detail_url}/{locality}/{flat_type}/{flat_number}/"
            
            flat_data = {
                'title': title,
                'image_url': image_url,
                'url': url,
            }

            yield flat_data


def scrap_flats():
    flats = []
    def crawler_results(signal, sender, item, response, spider):
        flats.append(item)
   
    dispatcher.connect(crawler_results, signal=signals.item_scraped)

    db = Database()
    db.create()
    process = CrawlerProcess()
    process.crawl(RealEstateSpider)
    process.start()

    db.insert_flats(flats)