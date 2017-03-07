import scrapy


class BlogSpider(scrapy.Spider):
    name = 'bla'
    start_urls = ['http://localhost:8000/']
    custom_settings = {'USER_AGENT':'DDW', 'DOWNLOAD_DELAY':2}

    def parse(self, response):
        for title in response.css('h2.entry-title'):
            yield {'title': title.css('a ::text').extract_first()}

        next_page = response.css('a ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)