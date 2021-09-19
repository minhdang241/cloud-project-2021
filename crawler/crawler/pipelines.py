import requests
from psycopg2 import pool
import psycopg2.extras
import re
import string
import json
import datetime

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from pydantic import BaseModel
from typing import Optional, Any, List
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline
from .resources import categorize_career, compute_embeddings, preprocess, extract_skills, update_careers_query, \
    upsert_job_query, send_email
from sentence_transformers import SentenceTransformer
from .settings import settings
import torch
import logging


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
        # Open DB connection pool
        self.conn_pool = pool.SimpleConnectionPool(1, 100,
                                                   database=settings.POSTGRES_DB_NAME,
                                                   user=settings.POSTGRES_USER,
                                                   password=settings.POSTGRES_PASSWORD,
                                                   host=settings.POSTGRES_HOST,
                                                   port=settings.POSTGRES_PORT,
                                                   )
        if (self.conn_pool):
            print("Connection pool created successfully")

        # Fetch careers
        conn = self.conn_pool.getconn()
        cur = conn.cursor()
        cur.execute('SELECT career_id, career_path FROM "Careers"')
        rows = cur.fetchall()
        cur.close()
        self.conn_pool.putconn(conn)
        self.career_dict = dict()
        for career_id, career_path in rows:
            self.career_dict[career_path] = int(career_id)

        # Load models
        checkpoint = "mrm8488/codebert-base-finetuned-stackoverflow-ner"
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        model = AutoModelForTokenClassification.from_pretrained(checkpoint)
        self.classifier = pipeline("token-classification", model=model, tokenizer=tokenizer)
        self.sent_model = SentenceTransformer('paraphrase-MiniLM-L12-v2')

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
            if career_path is None:
                return
            job.career = career_path
            job.career_id = self.career_dict[career_path]
            job.preprocessed_description = preprocess(job.description)
            job.skills = extract_skills(self.classifier, job.description)
            job.embeddings = compute_embeddings(self.sent_model, job.preprocessed_description)
            conn = self.conn_pool.getconn()
            cur = conn.cursor()
            job_dict = job.__dict__
            job_dict["skills"] = json.dumps(job_dict["skills"])
            job_dict["embeddings"] = json.dumps(job_dict["embeddings"])
            cur.execute(upsert_job_query, job_dict)
            conn.commit()
            cur.close()
            self.conn_pool.putconn(conn)
            return item

    def close_spider(self, spider):
        careers = self.calculate_careers()

        query_values = []
        for career in careers:
            query_values.append([career.career_id, career.total_jobs,
                                 json.dumps(list(career.skills)),
                                 json.dumps(career.embeddings)])

        conn = self.conn_pool.getconn()
        cur = conn.cursor()
        psycopg2.extras.execute_values(
            cur, update_careers_query, query_values
        )
        conn.commit()
        cur.close()
        self.conn_pool.putconn(conn)
        self.conn_pool.closeall()
        status = "finished"
        if settings.REQUEST_ID:
            payload = json.dumps({
                "request_id": settings.REQUEST_ID,
                "updated_at": str(datetime.datetime.utcnow()),
                "request_metadata": {
                    "total_item": len(self.ids_seen)
                },
                "status": "FINISHED"
            })
            try:
                requests.put(settings.UPDATE_REQUEST_URL, data=payload,
                             headers={"Authorization": f"Bearer {settings.ACCESS_TOKEN}",
                                      "Content-Type": "application/json; charset=utf-8"
                                      }
                             )
                # Send email after update DB successfully
            except Exception as e:
                logging.error("Error when update database")
                logging.error(e)
                status = "failed"

        send_email(settings, status)



    def calculate_careers(self) -> List[Career]:
        conn = self.conn_pool.getconn()
        cur = conn.cursor()

        select_jobs_query = """
            SELECT skills, embeddings, career, career_id  FROM "Jobs";
        """
        cur.execute(select_jobs_query)
        rows = cur.fetchall()
        cur.close()
        self.conn_pool.putconn(conn)

        # Calculate new career
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
            c.embeddings = torch.mean(torch.stack(c.embeddings_tensors, dim=0), dim=0).tolist()

        return list(new_career_dict.values())


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
