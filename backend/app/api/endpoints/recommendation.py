from collections import defaultdict

from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.api.dependencies import recommendation
from app.resources.utils import get_db
from app.schemas.recommendation import request, response
from typing import Optional, List
from app.api.securities.cognito_auth import UserInfo, auth

router = APIRouter()


@router.get("/careers", response_model=response.CareerRecommendationResponse)
def get_recommended_careers(
        course_ids: Optional[List[int]] = Query(None),
        topk: int = None,
        db_session: Session = Depends(get_db),
        user: UserInfo = Depends(auth.claim(UserInfo))
):
    results = recommendation.get_recommended_jobs(db_session, course_ids, topk=topk)
    hash_map = defaultdict(list)
    for job in results:
        hash_map[job.job_career.career_path].append(response.Job(**job.__dict__))

    career_list = []
    for career_path, jobs in hash_map.items():
        career_list.append(response.Career(career=career_path, job_list=jobs))
    return response.CareerRecommendationResponse(career_list=career_list)


@router.get("/mismatch_skills", response_model=response.MismatchSkillsRecommendationResponse)
def get_mismatch_skills(
        course_ids: Optional[List[int]] = Query(None),
        career_id: int = None,
        db_session: Session = Depends(get_db),
        user: UserInfo = Depends(auth.claim(UserInfo))
):
    matching_skills, missing_skills = recommendation.get_recommended_mismatch_skills(db_session, course_ids,
                                                                                     career_id)
    matching = []
    for skill in matching_skills:
        matching.append(response.Skill(name=skill))
    missing = []
    for skill in missing_skills:
        missing.append(response.Skill(name=skill))
    return response.MismatchSkillsRecommendationResponse(matching_skills=matching, missing_skills=missing)


@router.get("/courses", response_model=Page[response.SchoolCourse])
def get_recommended_courses(
        career_id: int,
        school_id: int,
        topk: int = None,
        db_session: Session = Depends(get_db),
        user: UserInfo = Depends(auth.claim(UserInfo))
):
    courses = recommendation.get_recommended_courses(db_session, career_id=career_id, school_id=school_id,
                                                     topk=topk)
    course_list = []
    for c in courses:
        course_list.append(response.SchoolCourse(**c.__dict__))
    return paginate(course_list)
