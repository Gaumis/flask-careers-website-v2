# from flask module we are importing Flask class
from flask import Flask, render_template, jsonify, request, redirect, url_for
from sqlalchemy import text
from database import engine, load_job_from_db, add_application_to_db
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
  image = "/static/banner.jpg"
  all_jobs = load_jobs_from_db()
  #print(all_jobs)
  return render_template('home.html', jobs=all_jobs, image=image)


@app.route("/api/jobs")
def list_jobs():
  return jsonify(load_jobs_from_db())


@app.route("/job/<id>")
def load_specific_job(id):
  image = "/static/banner.jpg"
  job = load_job_from_db(id)
  if not job:
    return "Not Found", 404
  return render_template('jobpage.html', job=job, image=image)


@app.route("/job/<id>/apply", methods=['post'])
def apply_to_job(id):
  print(f"job id is {id}")
  image = "/static/congratulation.jpg"
  data = request.form
  job = load_job_from_db(id)
  print(data)
  add_application_to_db(id, data)
  #store data in database
  #send automated email to candidate
  #display acknowledge mail to the candidate
  return render_template('application_confirmation.html',
                         application=data,
                         job=job, image=image, name=data['full_name'])

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  
        # Handle the login form submission
        username = request.form['username']
        password = request.form['password']
        # Implement your login logic here
        # Check if the username and password are valid
        # If valid, perform the login operation
        # Otherwise, display an error message

        # Redirect to the home page or a dashboard page after successful login
        return redirect(url_for('home'))
    
    # Render the login template
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle the register form submission
        username = request.form['username']
        password = request.form['password']
        # Implement your register logic here
        # Check if the username is available and password is valid
        # If valid, create a new user account
        # Otherwise, display an error message

        # Redirect to the login page after successful registration
        return redirect(url_for('login'))
    
    # Render the register template
    return render_template('registration_page.html')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=False)
