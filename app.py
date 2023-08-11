# from flask module we are importing Flask class
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from sqlalchemy import text
from database import load_jobs_from_db, load_job_from_db, add_user_to_db, get_password_for_user, change_password_for_user
from filters import inr_format
import secrets
# object of Flask class is created with __name__ which is equal to __main__
app = Flask(__name__)
app.debug = False
app.jinja_env.filters['inr_format'] = inr_format

app.secret_key=secrets.token_hex(16)

image = "/static/banner.jpg"
all_jobs = load_jobs_from_db()

# @ symbol is decorator
@app.route("/")
def hello_world():
  print(all_jobs)
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

# here I'll use AJAX fetch operation.
@app.route('/changePassword', methods=['POST','GET'])
def change_password():
   
   if request.method == "POST":
      # data = request.form
      # current_password=request.form['currentPassword']
      # change_password=request.form['newPassword']
      item_data = request.get_json(silent=True)
      if item_data is None:
        return jsonify({"message": "Invalid JSON data"}), 400
      current_password=item_data['currentPassword']
      change_password=item_data['newPassword']
      print("enter inside changePassword route")
      userid=session.get('userid')
      print(f"item_data : {item_data['currentPassword']}, new passwrod {item_data['newPassword']}")
      print(userid)
      mess, status_code = change_password_for_user(userid, current_password, change_password)
      if status_code==200:
         return jsonify({"message": "Items added successfully"})
      else:
         return jsonify({"message": "fail added successfully"})
      
   return render_template('change_password.html')
    

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  
        # Handle the login form submission
        print(f"login route for post")
        username = request.form['userEmailId']
        password = request.form['userPassword']
        print(username)
        getPassword, name, getUserId, status_code = get_password_for_user(username)
        print(f"heelo {getPassword}- {name} - {getUserId} - {status_code}")
        session['username']=username
        session['userid']=getUserId
        print(f"{getPassword}- {name} - {getUserId} - {status_code}")
        if status_code==200 and getPassword == password:
           return render_template('home.html', userName=name , jobs=all_jobs, image=image)
        else:
          return redirect(url_for('login'))
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
        data = request.form
        print(f"data for registration : -,{data}")
        userName = request.form['inputFullName']
        addedUser = add_user_to_db(data)
        return render_template('home.html', userName=userName , jobs=all_jobs, image=image)
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
