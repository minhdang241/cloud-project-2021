from typing import List, Set, Tuple

import torch
from fastapi.logger import logger
from sentence_transformers import util
from sqlalchemy.orm import Session

from app.crud import career, course, job
from app.crud.crud_career import CareerUpdate
from app.db.postgres import models
from app.db.postgres.setup_postgres import Base


def get_skills(obj_list: List[Base]) -> Set[str]:
    skill_set = set()
    for c in obj_list:
        skill_set.update(c.skills)
    return skill_set


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


def update_career(db_session: Session, career_id: int, skills: List[str], total_jobs: int = None):
    db_obj = career.get_by_id(db_session, id=career_id)
    if total_jobs:
        obj_in = CareerUpdate(
            skills=skills,
            total_jobs=total_jobs
        )
    else:
        obj_in = CareerUpdate(
            skills=skills,
        )
    obj = career.update(db_session, db_obj=db_obj, obj_in=obj_in)
    return obj


def get_recommended_mismatch_skills(db_session: Session, course_ids: List[int], career_id: int) -> Tuple[
    List[str], List[str]]:
    courses = course.filter_by(db_session, id=course_ids)
    logger.debug(courses)

    my_skills = get_skills(courses)
    career_skills = set(career.get_field_by_id(db_session, career_id, fields=['skills'])[0])
    logger.debug(career_skills)
    logger.debug(f"Total career skills: {len(career_skills)}")

    matching_skills = my_skills.intersection(career_skills)
    missing_skills = career_skills.difference(my_skills)
    return list(matching_skills), list(missing_skills)


def get_recommended_jobs(db_session: Session, data: List[int], topk: int = None) -> List[models.Job]:
    courses = course.filter_by(db_session, order_desc=True, id=data)
    logger.debug(courses)

    c_embed = calculate_course_embeddings(courses)
    logger.debug(f"Embedding length {len(c_embed)}")
    my_skills = get_skills(courses)

    jobs = job.get(db_session)
    logger.debug(f"Total jobs: {len(jobs)}")

    scores = []
    for j in jobs:
        job_embed = j.embeddings
        similarity_score = calculate_similarity_score(c_embed, job_embed)
        matching_skill_score = calculate_matching_skill_score(my_skills, j.skills)
        score = similarity_score * 0.6 + matching_skill_score * 0.4
        scores.append((j, score))
    scores.sort(key=lambda t: t[1], reverse=True)
    if topk:
        scores = scores[:topk]
    jobs = [t[0] for t in scores]
    return jobs


def get_recommended_courses(db_session: Session, career_id: int, school_id: int, topk: int = None) -> List[
    models.Course]:
    career_obj = career.get_field_by_id(db_session, career_id, fields=['embeddings', 'skills'])
    career_embed, career_skills = career_obj[0], career_obj[1]

    courses = course.filter_by(db_session, school_id=school_id)
    scores = []
    for c in courses:
        c_embed = c.embeddings
        similarity_score = calculate_similarity_score(c_embed, career_embed)
        matching_skill_score = calculate_matching_skill_score(set(c.skills), set(career_skills))
        score = similarity_score * 0.5 + matching_skill_score * 0.5
        scores.append((c, score))

    scores.sort(key=lambda t: t[1], reverse=True)
    if topk:
        scores = scores[:topk]
    courses = [t[0] for t in scores]
    return courses
