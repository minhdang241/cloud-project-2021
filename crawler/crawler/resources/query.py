upsert_job_query = """
    INSERT INTO "Jobs" (title, company_name, company_location, short_description, description, link, skills, embeddings, career_id, preprocessed_description, career)
    VALUES (%(title)s, %(company_name)s, %(company_location)s, %(short_description)s, %(description)s, %(link)s, %(skills)s, %(embeddings)s, %(career_id)s, %(preprocessed_description)s, %(career)s)
    ON CONFLICT (link) 
    DO UPDATE 
    SET title = %(title)s,
        company_name = %(company_name)s,
        company_location = %(company_location)s,
        short_description = %(short_description)s,
        description = %(description)s,
        link = %(link)s,
        skills = %(skills)s,
        embeddings = %(embeddings)s,
        career_id = %(career_id)s,
        preprocessed_description = %(preprocessed_description)s,
        career = %(career)s
"""

update_careers_query = """
    UPDATE "Careers" AS c
    SET 
        total_jobs = e.total_jobs,
        skills = CAST(e.skills as jsonb),
        embeddings = CAST(e.embeddings as jsonb) 
    FROM (VALUES %s) AS e(career_id, total_jobs, skills, embeddings) 
    WHERE c.career_id = e.career_id
"""