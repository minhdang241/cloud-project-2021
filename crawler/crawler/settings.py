BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

DOWNLOAD_DELAY = 2

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'crawler.pipelines.DuplicatesPipeline': 800,
    'crawler.pipelines.CleanPipeline': 300,
}