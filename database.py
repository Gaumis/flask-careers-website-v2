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
