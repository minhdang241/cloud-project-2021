from typing import List, Set

import torch
from fastapi.logger import logger
from sentence_transformers import util
from sqlalchemy.orm import Session

from app.crud import course, job
from app.db.postgres import models


def get_skills_from_course(courses: List[models.Course]) -> Set[str]:
    course_skills = set()
    for c in courses:
        course_skills.update(c.skills)
    return course_skills


def calculate_course_embeddings(courses: List[models.Course]) -> torch.Tensor:
    embeddings = [torch.Tensor(c.embeddings) for c in courses]
    c_embed = torch.mean(torch.stack(embeddings, dim=0), dim=0)
    return c_embed


def calculate_similarity_score(embed_1: torch.Tensor, embed_2: torch.Tensor) -> float:
    return util.pytorch_cos_sim(embed_1, embed_2).item()


def calculate_matching_skill_score(my_skills: Set[str], job_skills: Set[str]) -> float:
    mutual = my_skills.intersection(job_skills)
    if len(my_skills) != 0:
        return len(mutual) / len(my_skills)
    else:
        return 0


def get_recommended_jobs(db_session: Session, data, topk=None) -> List[models.Job]:
    courses = course.filter_by(db_session, order_desc=True, id=data)
    logger.debug(courses)

    c_embed = calculate_course_embeddings(courses)
    logger.debug(f"Embedding length {len(c_embed)}")
    my_skills = get_skills_from_course(courses)

    jobs = job.get(db_session)
    logger.debug(f"Total jobs: {len(jobs)}")

    scores = []
    for j in jobs:
        job_embed = j.embeddings
        similarity_score = calculate_similarity_score(c_embed, job_embed)
        matching_skill_score = calculate_matching_skill_score(my_skills, j.skills)
        score = similarity_score * 0.6 + matching_skill_score * 0.4
        scores.append((j, score))
    scores.sort(key=lambda t: t[1])
    if topk:
        scores = scores[:topk]
    jobs = [t[0] for t in scores]
    return jobs
