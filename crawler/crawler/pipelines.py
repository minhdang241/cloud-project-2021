import re
import string

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class JobDuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['link'] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter['link'])
            return item

class DuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['code'] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter['code'])
            return item
        
        
class CleanPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        keys = ["code", "title", "description", "outcome"]
        for key in keys:
            if adapter.get(key):
                clean_text = adapter[key].strip(string.punctuation + " ")
                adapter[key] = re.sub('\s{2,}', ' ', clean_text)
        return item