import scrapy

from scrapy.loader import ItemLoader
from ..items import SantanderconsumerplItem
from itemloaders.processors import TakeFirst


class SantanderconsumerplSpider(scrapy.Spider):
	name = 'santanderconsumerpl'
	start_urls = ['https://www.blog.santanderconsumer.pl/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="small-content"]')
		for post in post_links:
			url = post.xpath('./div[@class="buttons-line"]/a/@href').get()
			date = post.xpath('./div[@class="public-data"]/text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date})

	def parse_post(self, response, date):
		title = response.xpath('//h1[@class="main-title"]/text()').get()
		description = response.xpath('//div[contains(@class, "desc-module")]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=SantanderconsumerplItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
