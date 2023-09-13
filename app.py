# from flask module we are importing Flask class
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from sqlalchemy import text
from database import engine, load_job_from_db, add_application_to_db, get_password_for_user, change_password_for_user, add_user_to_db, check_user_in_db, check_if_already_applied, get_applied_applications, db_get_all_application, get_candidate_details_with_jobs, take_action_db
from filters import inr_format
import secrets

# object of Flask class is created with __name__ which is equal to __main__
app = Flask(__name__)
app.debug = False
app.jinja_env.filters['inr_format'] = inr_format

app.secret_key=secrets.token_hex(16)

def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    jobs = []
    for row in result:
      jobs.append(dict(zip(result.keys(), row)))
  return jobs

all_jobs = load_jobs_from_db()
image = "/static/banner.jpg"


# @ symbol is decorator
@app.route("/")
def hello_world():
  username = session.get('userName')
  image = "/static/banner.jpg"
  all_jobs = load_jobs_from_db()
  #print(all_jobs)
  if username:
    return render_template('home.html', jobs=all_jobs, image=image, userName = username)
  else:
    return render_template('home.html', jobs=all_jobs, image=image)

@app.route("/logout")
def logout():
  username = session.get('userName')
  print(f"userName : {username}")
  session.clear()
  return redirect(url_for('hello_world'))

@app.route("/api/jobs")
def list_jobs():
  return jsonify(load_jobs_from_db())


@app.route('/gaumisAPI/getAllApplication/<id>')
def get_all_application(id):
  print(f"Fetching jobs application for job id : {id}")
  return jsonify(db_get_all_application(id))

@app.route('/<job_id>/<application_id>')
def load_job_application(job_id, application_id):
  userRole = session.get('userRole')
  username = session.get('userName')
  print(f"userRole : {userRole}")
  if userRole == 'ADMIN':
    candidate_detail=get_candidate_details_with_jobs(application_id)
    print(f"candidate_detail is {candidate_detail[0]['title']}")
    return render_template('admin_applicationView.html', userName=username, candidate=candidate_detail[0])
  else:
    return render_template('AdminError.html')


@app.route("/job/<id>")
def load_specific_job(id):
  username = session.get('userName')
  userEmail = session.get('userEmail')
  print(f"userName : {username}, userEmail : {userEmail}")
  image = "/static/banner.jpg"
  message = "Login, Before you can apply for Job"
  job = load_job_from_db(id)
  if username:
    return render_template('jobpage.html', job=job, image=image, userName=username, userEmail=userEmail )
  else:
    return render_template('login.html', messages=message)

@app.route("/applicationStatus")
def application_status():
  userEmail = session.get('userEmail')
  username = session.get('userName')
  list_of_applications = get_applied_applications(userEmail)
  enumerated_applications = list(enumerate(list_of_applications, start=1))
  if list_of_applications:
    return render_template('application_status.html', applications = enumerated_applications, userName=username)
  else:
    return None

@app.route("/job/<id>/apply", methods=['post'])
def apply_to_job(id):
  username = session.get('userName')
  userEmail = session.get('userEmail')
  print(f"job id is {id}")
  image = "/static/congratulation.jpg"
  data = request.form
  job = load_job_from_db(id)
  print(data)
  userExist = check_if_already_applied(id, userEmail)
  if userExist:
    add_application_to_db(id, data)
    return render_template('application_confirmation.html',
                         application=data,
                         job=job, image=image, name=data['full_name'], userName=username)
  else:
    return {"message":f"you have already applied for job id {id}"}

  #store data in database
  #send automated email to candidate
  #display acknowledge mail to the candidate
  

# here I'll use AJAX fetch operation.
@app.route('/changePassword', methods=['POST','GET'])
def change_password(): 
  if request.method == "POST":
    # data = request.form
    # current_password=request.form['currentPassword']
    # change_password=request.form['newPassword']
    item_data = request.get_json(silent=True)
    print(item_data)
    if item_data is None:
      return jsonify({"message": "Invalid JSON data Gaurav"}), 400
    current_password=item_data['currentPassword']
    change_password=item_data['newPassword']
    
    print("enter inside changePassword route")
    userid=session.get('userid')
    print(f"item_data : {item_data['currentPassword']}, new password {item_data['newPassword']}")
    print(f"userid is : {userid}")
    mess, status_code = change_password_for_user(userid, current_password, change_password)
    print(f"Message is {mess}, Status code is {status_code}")
    if status_code == 200:
      print("Hi Gaurav")
      return jsonify({"message": "Password Changed Successfully"}), 200
    else:
       return jsonify({"message": "Password Change is Unsuccessful, Try Again!"}), 400
  
  return render_template('change_password.html')



@app.route('/takeAction', methods=['POST'])
def take_action():
  print("Application Status is changed")
  item_data = request.get_json()
  appId=item_data['application_id']
  appStatus=item_data['status']
  data, status_code=take_action_db(appId, appStatus)
  return data

applications = [
            {
                'full_name': 'John Doe',
                'email': 'john@example.com',
                'work_experience': '3 years',
                # Other application details
            },
            {
                'full_name': 'Jane Smith',
                'email': 'jane@example.com',
                'work_experience': '5 years',
                # Other application details
            },
            # More applications for Data Analyst
        ]

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    # Handle the login form submission
    print(f"login route for post")
    username = request.form['userEmailId']
    password = request.form['userPassword']
    print(f"Enter username : {username} and password : {password}")
    getPassword, name, getUserId, userRole, status_code, = get_password_for_user(username)
    print(f"heelo {getPassword}- {name} - {getUserId} - {status_code}- {userRole}")
    session['userName']=name
    session['userEmail']=username
    session['userid']=getUserId
    session['userRole']=userRole
    print(f"{getPassword}- {name} - {getUserId} - {status_code}")
    print(f"userRole : {userRole} and type is {type(userRole)}")
    print(all_jobs)

    if status_code==200 and getPassword == password and userRole=='ADMIN':
      print("Admin Logged in: ")
      return render_template('ADMIN.html', userName=name , jobs=all_jobs, applications=applications, isAdmin="isAdmin")
    elif status_code==200 and getPassword == password:
      return render_template('home.html', userName=name , jobs=all_jobs, image=image)  
    elif getPassword != password:
      message = "Enter password doesn't match"
      return render_template('login.html', messaged=message)
    else:
      return redirect(url_for('login'))
    # Implement your login logic here
    # Check if the username and password are valid
    # If valid, perform the login operation
    # Otherwise, display an error message
    # Redirect to the home page or a dashboard page after successful login
  
  # Render the login template
  return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle the register form submission
        # username = request.form['username']
        # password = request.form['password']
        data = request.form
        print(f"data for registration : -,{data}")
        userName = request.form['inputFullName']
        userEmail = request.form['inputEmailId']
        userExist = check_user_in_db(userEmail)
        if userExist:
          addedUser = add_user_to_db(data)
          return render_template('home.html', userName=userName , jobs=all_jobs, image=image)
        else:
          message = "Username Already! Exist"
          return render_template('registration_page.html', message = message)
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