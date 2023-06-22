# from flask module we are importing Flask class
from flask import Flask, render_template, jsonify

# object of Flask class is created with __name__ which is equal to __main__
app = Flask(__name__)

JOBS = [{
  'id': 1,
  'title': 'Data Analyst',
  'location': 'Bengaluru, India',
  'salary': '10,00,000'
}, {
  'id': 2,
  'title': 'Data Scientist',
  'location': 'Delhi, India',
  'salary': '15,00,000'
}, {
  'id': 3,
  'title': 'Frontend Developer',
  'location': 'Remote'
}, {
  'id': 4,
  'title': 'Backend Developer',
  'location': 'San Fransico, USA',
  'salary': '$120,000'
}]


# @ symbol is decorator
@app.route("/")
def hello_world():
  return render_template('home.html', jobs=JOBS)


@app.route("/api/jobs")
def list_jobs():
  return jsonify(JOBS)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
