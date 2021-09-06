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
from typing import Any, Optional
import psycopg2
from pydantic import BaseModel

class Career(BaseModel):
    career_id: int
    career_path: str
    skills: Optional[Any] = None
    total_job: Optional[int] = 0
    embeddings: Optional[Any] = None

conn = psycopg2.connect(
    dbname="cloud",
    user="postgres",
    password="nB7geYEjbFT3UBUKJqfKkPuHpkKsUVsWmaDcrTdd6d6HpkKsUVsWmDaQDxJqfKkPu",
    host="localhost",
    port="10000",
)

cur = conn.cursor()

# cur.execute('SELECT * FROM "Jobs" WHERE "Jobs".link = %s', ('https://www.indeed.com/rc/clk?jk=2903924ed4aaad4b&fccid=bb23b4fe03789986&vjs=3',))
cur.execute('SELECT * FROM "Careers"')
rows = cur.fetchall()
careers = list()
for row in rows:
    c = Career(career_id=int(row[3]),
                career_path=row[0],
                skills=row[1],
                total_job=int(row[2]),
                embeddings=row[4])
    careers.append(c)
for c in careers:
    print(c.career_path)