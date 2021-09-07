def categorize_career(job_title):
    job_title = job_title.lower()
    if "frontend" in job_title:
        return "Frontend Engineer"
    if "backend" in job_title:
        return "Backend Engineer"
    if "full" in job_title and "stack" in job_title:
        return "Full-stack Engineer"
    if "ios" in job_title:
        return "IOS Developer"
    if "android" in job_title:
        return "Android Developer"
    if "cyber" in job_title:
        return "Cyber Security"
    if "test" in job_title or "qa" in job_title:
        return "Software Tester"
    if "machine learning" in job_title or "ai" in job_title:
        return "ML/AI Engineer"
    if "devops" in job_title:
        return "DevOps"
    if "web" in job_title:
        return "Web Developer"
    if "data" in job_title:
        return "Data Engineer"
    if "software" in job_title:
        return "Software Engineer"
    return None