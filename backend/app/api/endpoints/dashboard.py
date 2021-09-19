import string

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.resources.utils import get_db
from app.schemas.dashboard import response
from app import crud
from collections import Counter
from typing import Optional
from app.resources.strings import STOP_WORDS

router = APIRouter()


@router.get("/courses/levels")
def get_course_level(
        db_session: Session = Depends(get_db)
):
    return crud.course.get_course_level_count(db_session)


@router.get("/courses/word-cloud", response_model=response.WordFrequencies)
def get_course_word_cloud(
        db_session: Session = Depends(get_db)
):
    objs = crud.course.get(db_session, fields=["preprocessed_description"])

    words = []
    for o in objs:
        for c in o.preprocessed_description.split():
            if c.lower() not in STOP_WORDS and c not in string.punctuation:
                words.append(c.lower())

    counter = Counter(" ".join(words).split()).most_common(60)
    return response.WordFrequencies(
        words=[response.WordFreq(value=value, count=count) for (value, count) in counter])


@router.get("/jobs/company", response_model=response.WordFrequencies)
def get_job_company_count(
        db_session: Session = Depends(get_db)
):
    objs = crud.job.get_job_company_count(db_session)
    new_list = sorted(objs, key=lambda x: x.count, reverse=True)
    print(new_list)
    return response.WordFrequencies(
        words=[response.WordFreq(value=o.company_name, count=o.count) for o in new_list[:20]])


@router.get("/jobs/word-cloud", response_model=response.WordFrequencies)
def get_job_word_cloud(
        career_id: Optional[int] = None,
        db_session: Session = Depends(get_db)
):
    if career_id:
        objs = crud.job.get(db_session, fields=["preprocessed_description"], career_id=career_id)
    else:
        objs = crud.job.get(db_session, fields=["preprocessed_description"])

    words = []
    for o in objs:
        for c in o.preprocessed_description.split():
            if c not in STOP_WORDS and c not in string.punctuation:
                words.append(c)

    counter = Counter(" ".join(words).split()).most_common(60)
    return response.WordFrequencies(
        words=[response.WordFreq(value=value, count=count) for (value, count) in counter])


@router.get("/jobs/district")
def get_job_district_count(
        db_session: Session = Depends(get_db)
):
    return crud.job.get_job_district_count(db_session)


@router.get("/counts", response_model=response.Counts)
def get_counts(
        db_session: Session = Depends(get_db)
):
    return response.Counts(
        course_count=crud.course.get_course_count(db_session),
        job_count=crud.job.get_job_count(db_session),
        company_count=crud.job.get_company_count(db_session),
        career_count=crud.career.get_career_count(db_session)
    )
