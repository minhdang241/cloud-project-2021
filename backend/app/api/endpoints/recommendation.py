from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import recommendation
from app.resources.utils import get_db
from app.schemas.recommendation import request, response

router = APIRouter()


@router.post("/careers", response_model=response.CareerRecommendationResponse)
def generate_recommended_career(
        data: request.CareerRecommendationRequest,
        db_session: Session = Depends(get_db),
):
    course_ids = [course.course_id for course in data.course_list]
    results = recommendation.get_recommended_jobs(db_session, course_ids, topk=data.topk)
    hash_map = defaultdict(list)
    for job in results:
        hash_map[job.career].append(response.Job(**job.__dict__))
    career_list = []
    for career, jobs in hash_map.items():
        career_list.append(response.Career(career=career, job_list=jobs))
    return response.CareerRecommendationResponse(career_list=career_list)
