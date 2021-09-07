import psycopg2
import re
import string
import json

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from pydantic import BaseModel
from typing import Optional, Any, List
from .resources.career import categorize_career
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline
from .resources.skills import extract_skills
from .resources.preprocess import preprocess
from .resources.embeddings import compute_embeddings
from .resources.query import upsert_job_query, update_careers_query
import torch

class Job(BaseModel):
    # job_id: int
    title: str
    company_name: str
    company_location: str
    short_description: str
    description: str
    link: str
    skills: Optional[Any] = None
    embeddings: Optional[Any] = None
    career_id: Optional[int] = None
    career: Optional[str] = None
    preprocessed_description: Optional[str] = None


class Career(BaseModel):
    career_id: int
    career_path: str
    skills = set()
    total_jobs = 0
    embeddings = list()
    embeddings_tensors = list()

class JobDuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()
    
    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            dbname="cloud",
            user="postgres",
            password="nB7geYEjbFT3UBUKJqfKkPuHpkKsUVsWmaDcrTdd6d6HpkKsUVsWmDaQDxJqfKkPu",
            host="localhost",
            port="10000",
        )
        cur = self.conn.cursor()
        cur.execute('SELECT career_id, career_path FROM "Careers"')
        rows = cur.fetchall()
        self.career_dict = dict()
        for career_id, career_path in rows:
            self.career_dict[career_path] = career_id
        cur.close()
        checkpoint = "mrm8488/codebert-base-finetuned-stackoverflow-ner"
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        model = AutoModelForTokenClassification.from_pretrained(checkpoint)
        self.classifier = pipeline("token-classification", model=model, tokenizer=tokenizer)


    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['link'] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter['link'])
            """
            Process the item and store to database.
            """
            job = Job(**item)
            career_path = categorize_career(job.title)
            job.career = career_path
            job.career_id = self.career_dict[career_path]
            job.preprocessed_description = preprocess(job.description)
            job.skills = extract_skills(self.classifier, job.description)
            job.embeddings = compute_embeddings(job.preprocessed_description)
            cur = self.conn.cursor()
            cur.execute(upsert_job_query, job.__dict__)
            self.conn.commit()
            cur.close()
            
            return item
        
    def close_spider(self, spider):
        careers = self.calculate_careers()
        
        cur = self.conn.cursor()
        query_values = []
        for career in careers:
            query_values.append([career.career_id, career.total_jobs, 
                                json.dumps(list(career.skills)), 
                                json.dumps(career.embeddings)])

        psycopg2.extras.execute_values(
            cur, update_careers_query, query_values
        )
        self.conn.commit()
        cur.close()
        self.conn.close()
        
    def calculate_careers(self) -> List[Career]:
        cur = self.conn.cursor()
        
        # Calculate new career
        select_jobs_query = """
            SELECT skills, embeddings, career, career_id  FROM "Jobs";
        """
        cur.execute(select_jobs_query)
        rows = cur.fetchall()
        new_career_dict = dict()
        for skills, embeddings, career, career_id in rows:
            if career_id not in new_career_dict:
                new_career_dict[career_id] = Career(
                    career_id=career_id,
                    career_path=career
                )
            career: Career = new_career_dict[career_id]
            career.total_jobs += 1
            if skills:
                career.skills.update(skills)
            if embeddings:
                career.embeddings_tensors.append(torch.Tensor(embeddings))
        for c in new_career_dict.values():
            c.embeddings = torch.mean(torch.stack(c.embeddings_tensors, dim=0), dim=0)
        cur.close()
        return new_career_dict.values()

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