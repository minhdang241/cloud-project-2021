import psycopg2
import re
import string

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from pydantic import BaseModel
from typing import Optional, Any

class Job(BaseModel):
    job_id: int
    title: str
    company_name: str
    company_location: str
    short_description: str
    description: str
    link: str
    skills: Optional[Any] = None
    embeddings: Optional[Any] = None
    career_id: int
    preprocessed_description: str


class Career(BaseModel):
    career_id: int
    career_path: str
    skills: Optional[Any] = None
    total_job: Optional[int] = 0
    embeddings: Optional[Any] = None

class JobDuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()
        self.conn = psycopg2.connect(
            dbname="cloud",
            user="postgres",
            password="nB7geYEjbFT3UBUKJqfKkPuHpkKsUVsWmaDcrTdd6d6HpkKsUVsWmDaQDxJqfKkPu",
            host="localhost",
            port="10000",
        )
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM "Careers"')
        rows = cur.fetchall()
        careers = dict()
        for row in rows:
            c = Career(career_id=int(row[3]),
                        career_path=row[0],
                        skills=row[1],
                        embeddings=row[4])
            careers[c.career_path] = c
        self.careers = careers


    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['link'] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter['link'])
            """
            Process the item and store to database.
            """
            cur = self.conn.cursor()
            cur.execute('SELECT * FROM "Jobs" WHERE "Jobs".link = %s', (adapter['link'],))

            row = cur.fetchone()
            if len(row) == 1:
                self.log("EXIST")
                self.log(row)
                return
            self.log("NOT EXIST")
            
            # job = Job(**item)
            # self.log(job)

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