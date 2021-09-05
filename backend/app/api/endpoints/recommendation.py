from collections import defaultdict

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.api.dependencies import recommendation
from app.resources.utils import get_db
from app.schemas.recommendation import request, response

router = APIRouter()


@router.post("/careers", response_model=response.CareerRecommendationResponse)
def get_recommended_careers(
        data: request.CareerRecommendationRequest,
        db_session: Session = Depends(get_db),
):
    course_ids = [course.course_id for course in data.course_list]
    results = recommendation.get_recommended_jobs(db_session, course_ids, topk=data.topk)
    hash_map = defaultdict(list)
    for job in results:
        hash_map[job.career.career_path].append(response.Job(**job.__dict__))

    career_list = []
    for career_path, jobs in hash_map.items():
        career_list.append(response.Career(career=career_path, job_list=jobs))
    return response.CareerRecommendationResponse(career_list=career_list)


@router.post("/mismatch_skills", response_model=response.MismatchSkillsRecommendationResponse)
def get_mismatch_skills(
        data: request.MismatchSkillsRecommendationRequest,
        db_session: Session = Depends(get_db)
):
    course_ids = [course.course_id for course in data.course_list]
    matching_skills, missing_skills = recommendation.get_recommended_mismatch_skills(db_session, course_ids,
                                                                                     data.career_id)
    matching = []
    for skill in matching_skills:
        matching.append(response.Skill(name=skill))
    missing = []
    for skill in missing_skills:
        missing.append(response.Skill(name=skill))
    return response.MismatchSkillsRecommendationResponse(matching_skills=matching, missing_skills=missing)


@router.post("/courses", response_model=Page[response.SchoolCourse])
def get_recommeded_courses(
        data: request.CourseRecommendationRequest,
        db_session: Session = Depends(get_db)
):
    courses = recommendation.get_recommended_courses(db_session, career_id=data.career_id, school_id=data.school_id,
                                                     topk=data.topk)
    course_list = []
    for c in courses:
        course_list.append(response.SchoolCourse(**c.__dict__))
    return paginate(course_list)
