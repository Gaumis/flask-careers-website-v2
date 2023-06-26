import os
from sqlalchemy import create_engine, text

connection_string = os.environ['CONNECTION_STRING']

engine = create_engine(connection_string)


def load_job_from_db(id):
  with engine.connect() as conn:
    statement = text("SELECT * FROM jobs WHERE id = :id")
    result = conn.execute(statement, {"id": id})
    job = result.fetchone()
  if job:
    return dict(zip(result.keys(), job))
  else:
    return None


def add_application_to_db(job_id, data):
  with engine.connect() as conn:
    statement = text(
      "INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) values (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)"
    )
    result = conn.execute(
      statement, {
        "job_id": job_id,
        "full_name": data['full_name'],
        "email": data['email'],
        "linkedin_url": data['linkedin_url'],
        "education": data['education'],
        "work_experience": data['work_experience'],
        "resume_url": data['resume_url']
      })

def select_row_from_db(jod_id):
  with engine.connect() as conn:
    select_statement = text("SELECT * FROM applications WHERE job_id = :job_id")
    select_result = conn.execute(select_statement, {"job_id": jod_id})
    inserted_data = select_result.fetchone()
    print("Inserted data:", inserted_data)

