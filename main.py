
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "wiki"
    start_urls = [
        'https://en.wikipedia.org/wiki/Color_vision',
    ]
    custom_settings = {'USER_AGENT': 'DDW_friendly_bot', 'DOWNLOAD_DELAY': 2,
                       'DEPTH_LIMIT':5}

    def parse(self, response):
        # for quote in response.css('div.quote'):
        #     yield {
        #         'text': quote.css('span.text::text').extract_first(),
        #         'author': quote.css('small.author::text').extract_first(),
        #         'tags': quote.css('div.tags a.tag::text').extract(),
        #     }

        next_pages_raw = response.selector.xpath('//*/a[2]/@href').extract()
        next_pages = [page for page in next_pages_raw if page.startswith('/wiki/')]
        for next_page in next_pages:
            if next_page is not None:
                print('NEXT PAGE: ', next_page)
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
