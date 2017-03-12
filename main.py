
import scrapy
from scrapy.selector import Selector


class QuotesSpider(scrapy.Spider):
    name = "wiki"
    start_urls = [
        'https://en.wikipedia.org/wiki/Color_vision',
    ]
    custom_settings = {'USER_AGENT': 'DDW_friendly_bot', 'DOWNLOAD_DELAY': 2,
                       'DEPTH_LIMIT':5}

    def parse(self, response):
        h1 = response.css('h1.firstHeading::text').extract()[0]
        # content = response.css('#bodyContent').extract()
        first_paragraph = response.css('p').extract_first()
        yield {
            'title': h1,
            'first_paragraph': first_paragraph,
        }

        next_pages_raw = response.selector.xpath('//*/a[2]/@href').extract()
        next_pages = [page for page in next_pages_raw if page.startswith('/wiki/')]
        for next_page in next_pages:
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
