# from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
# from sqlalchemy.engine.base import Engine
# from sqlalchemy.engine.url import URL
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.dialects.postgresql import JSONB
# from sqlalchemy_json import mutable_json_type
# from sqlalchemy.orm import relationship
# from sqlalchemy.orm import sessionmaker


# password = 'nB7geYEjbFT3UBUKJqfKkPuHpkKsUVsWmaDcrTdd6d6HpkKsUVsWmDaQDxJqfKkPu'
# db_string = f"postgresql://backend:{password}@localhost:10000/cloud"

# DeclarativeBase = declarative_base()


# class Job(DeclarativeBase):
#     __tablename__ = "Jobs"
#     id = Column("job_id", Integer, primary_key=True)
#     title = Column(String)
#     company_name = Column(String)
#     company_location = Column(String)
#     short_description = Column(String)
#     description = Column(String)
#     link = Column(String)
#     skills = Column("skills", mutable_json_type(dbtype=JSONB, nested=True))
#     embeddings = Column("embeddings", mutable_json_type(dbtype=JSONB, nested=True))
#     career_id = Column(Integer, ForeignKey("Careers.career_id"))
#     preprocessed_description = Column(String)
    
# class Career(DeclarativeBase):
#     __tablename__ = "Careers"
#     id = Column("career_id", Integer, primary_key=True)
#     career_path = Column(String)
#     skills = Column("skills", mutable_json_type(dbtype=JSONB, nested=True))
#     total_jobs = Column(Integer)
#     jobs = relationship("Job", cascade="delete", backref="career")
#     embeddings = Column("embeddings", mutable_json_type(dbtype=JSONB, nested=True))

# engine = create_engine(
#     db_string,
#     pool_pre_ping=True
# )
# # each instance of this class will be the database session.
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# db = SessionLocal()
# print('ddd')
# # instance = db.query(Job).first()
# # print(instance)
# # db.flush()
# # db.close()
from collections import defaultdict
from typing import Any, Optional, List
import psycopg2
import psycopg2.extras
from pydantic import BaseModel
import json

class Career(BaseModel):
    career_id: int
    career_path: str
    skills = set()
    total_jobs = 0
    embeddings = list()
    embeddings_list = list()
    
class Job(BaseModel):
    # job_id: int
    title: str = "hehell"
    company_name: str = "name"
    company_location: str = "na"
    short_description: str = "na"
    description: str = "des"
    link: str = "test"
    skills: Optional[Any] = None
    embeddings: Optional[Any] = None
    career_id: Optional[int] = 1
    preprocessed_description: Optional[str] = None

conn = psycopg2.connect(
    dbname="cloud",
    user="postgres",
    password="nB7geYEjbFT3UBUKJqfKkPuHpkKsUVsWmaDcrTdd6d6HpkKsUVsWmDaQDxJqfKkPu",
    host="localhost",
    port="10000",
)

cur = conn.cursor()
career = Career(career_id = 13, career_path='', total_jobs=2, skills=['na', 'test'], embeddings=[0.1, 0.2])
cs = [career]
query_values = []
for c in cs:
     query_values.append([career.career_id, career.total_jobs, 
                          json.dumps(list(career.skills)), 
                          json.dumps(career.embeddings)])

update_query = """
    UPDATE "Careers" AS c
    SET 
        total_jobs = e.total_jobs,
        skills = CAST(e.skills as jsonb),
        embeddings = CAST(e.embeddings as jsonb) 
    FROM (VALUES %s) AS e(career_id, total_jobs, skills, embeddings) 
    WHERE c.career_id = e.career_id
"""

psycopg2.extras.execute_values(
cur, update_query, query_values
)
conn.commit()

# cur.execute('SELECT career_id, career_path FROM "Careers"')
# rows = cur.fetchall()
# career_dict = dict()
# for career_id, career_path in rows:
#     career_dict[career_path] = career_id

# print(career_dict)
# select_jobs_query = """
#     SELECT skills, embeddings, career, career_id  FROM "Jobs";
# """
# cur.execute(select_jobs_query)
# rows = cur.fetchall()
# new_career_dict = dict()
# for skills, embeddings, career, career_id in rows:
#     if career_id not in new_career_dict:
#         new_career_dict[career_id] = Career(
#             career_id=career_id,
#             career_path=career
#         )
#     career: Career = new_career_dict[career_id]
#     career.total_jobs += 1
#     if skills:
#         career.skills.update(skills)
#     if embeddings:
#         career.embeddings_list.append(embeddings)

# for career_id, career in new_career_dict.items():
#     print(career_id, career.career_path, career.total_jobs)
