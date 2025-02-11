import scrapy

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    image = scrapy.Field()
    description = scrapy.Field()
