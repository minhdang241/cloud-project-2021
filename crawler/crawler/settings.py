import os

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

DOWNLOAD_DELAY = 0.5

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# DATABASE = {
#     "drivername": "postgres",
#     "host": os.environ["POSTGRES_HOST"],
#     "port": os.environ["POSTGRES_PORT"],
#     "username": os.environ["POSTGRES_USER"],
#     "password": os.environ["POSTGRES_PASS"],
#     "database": os.environ["POSTGRES_DB"],
# }

DATABASE = {
    "drivername": "postgresql",
    "host": 'localhost',
    "port": '10000',
    "username": 'backend',
    "password": 'nB7geYEjbFT3UBUKJqfKkPuHpkKsUVsWmaDcrTdd6d6HpkKsUVsWmDaQDxJqfKkPu',
    "database": 'cloud',
}