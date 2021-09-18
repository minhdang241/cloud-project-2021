from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.resources.utils import get_db
from app.schemas.sample import request, response
from fastapi_pagination import Params, Page
from typing import Optional
from app import crud
router = APIRouter()


@router.get("/schools", response_model=Page[response.SchoolDTO])
def get_schools(
        paging_params: Params = Depends(),
        db_session: Session = Depends(get_db),
) -> Page[response.SchoolDTO]:
    return crud.school.get(db_session, paging_params)


@router.get("/schools/school_id/courses", response_model=Page[response.CourseDTO])
def get_school_courses(
        school_id: int,
        paging_params: Params = Depends(),
        db_session: Session = Depends(get_db),
) -> Page[response.CourseDTO]:
    return crud.course.get_by_fields(db_session, paging_params=paging_params, school_id=school_id)


@router.get("/courses", response_model=Page[response.CourseDTO])
def get_courses(
        level: Optional[str] = None,
        title: Optional[str] = None,
        sorted_by: Optional[str] = None,
        order: Optional[str] = None,
        paging_params: Params = Depends(),
        db_session: Session = Depends(get_db),
) -> Page[response.CourseDTO]:
    order_asc = False if order and order.lower() == "desc" else True
    return crud.course.get_courses(db_session, order_asc=order_asc, paging_params=paging_params,
                                   sorted_by=sorted_by, level=level, title=title)


@router.get("/jobs", response_model=Page[response.JobDTO])
def get_jobs(
        career_id: Optional[int] = None,
        paging_params: Params = Depends(),
        db_session: Session = Depends(get_db),
) -> Page[response.JobDTO]:
    if career_id:
        return crud.job.get(db_session, paging_params=paging_params, career_id=career_id)
    return crud.job.get(db_session, paging_params=paging_params)


@router.get("/careers", response_model=Page[response.CareerDTO])
def get_careers(
        paging_params: Params = Depends(),
        db_session: Session = Depends(get_db)
) -> Page[response.CareerDTO]:
    return crud.career.get(db_session, paging_params=paging_params)


@router.get("/courses/levels")
def get_course_level(
        db_session: Session = Depends(get_db)
):
    return crud.course.get_course_level_count(db_session)
