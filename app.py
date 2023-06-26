# from flask module we are importing Flask class
from flask import Flask, render_template, jsonify
from sqlalchemy import text
from database import engine, load_job_from_db
from filters import inr_format
# object of Flask class is created with __name__ which is equal to __main__
app = Flask(__name__)
app.debug = False
app.jinja_env.filters['inr_format'] = inr_format


def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    jobs = []
    for row in result:
      jobs.append(dict(zip(result.keys(), row)))
  return jobs


# @ symbol is decorator
@app.route("/")
def hello_world():
  all_jobs = load_jobs_from_db()
  print(all_jobs)
  return render_template('home.html', jobs=all_jobs)


@app.route("/api/jobs")
def list_jobs():
  return jsonify(load_jobs_from_db())


@app.route("/job/<id>")
def load_specific_job(id):
  job = load_job_from_db(id)
  if not job:
    return "Not Found", 404
  return render_template('jobpage.html', job=job)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=False)
