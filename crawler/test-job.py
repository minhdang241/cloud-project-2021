from typing import Any, Optional, List
import psycopg2
import psycopg2.extras
from pydantic import BaseModel
import torch

class Career(BaseModel):
    career_id: int
    career_path: str
    skills = set()
    total_jobs = 0
    embeddings = list()
    embeddings_tensors = list()
    
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

def calculate_careers(conn) -> List[Career]:
    cur = conn.cursor()
    
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
        c.embeddings = torch.mean(torch.stack(c.embeddings_tensors, dim=0), dim=0).tolist()
    cur.close()
    return new_career_dict.values()

print(calculate_careers(conn)[0])
