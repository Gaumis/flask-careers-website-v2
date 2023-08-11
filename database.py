import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()
print(os.getenv("HOST"),os.getenv("DATABASE"),os.getenv("USER_NAME"),os.getenv("PASSWORD"))

cnx = mysql.connector.connect(
host=os.getenv("HOST"),
database=os.getenv("DATABASE"),
user=os.getenv("USER_NAME"),
password=os.getenv("PASSWORD")
)

cursor = cnx.cursor()
# cursor.execute("SELECT * FROM jobs")
# result = cursor.fetchall()
# print(result)
print("my sql connector:  connection is successful")

def load_jobs_from_db():
  cursor.execute("SELECT * FROM jobs")
  jobs = cursor.fetchall()
  if jobs:
      column_names = [desc[0] for desc in cursor.description]
      job_list = [dict(zip(column_names, job)) for job in jobs]
      return job_list
  else:
      return None


def load_job_from_db(id):
  cursor.execute(f"select * from jobs where id={id}")
  job = cursor.fetchone()
  print(job)
  if job:
    column_names = [desc[0] for desc in cursor.description]
    print(column_names)
    return dict(zip(column_names, job))
  else:
    return None

def check_password(user):
  cursor.execute("select * from user ")
  data = cursor.fetchall()
  print(data)


def get_password_for_user(username):
  try: 
    print(f"username is {username}")
    cursor.execute(f"select userPassword, userFullName, userId from users where userEmailId ='{username}'")
    final_result = cursor.fetchone()
    print(final_result)
    print(f"final result, {final_result[0]}")
    return final_result[0], final_result[1], final_result[2], 200
  
  except Exception as e:
    print(f"User doesn't exist")
    return {"message":f"{username} User Not Found!"}, 404


def change_password_for_user(userid, current_password, change_password):
  try:
    while cursor.nextset():
      pass
    print(f"User id is {userid}")
    print(type(userid))
    cursor.execute(f"select userPassword from users where userId={userid}")
    result = cursor.fetchall()
    print(f"result is {result}")
    db_password=result[0][0]
    print(f"password is : {db_password}")
    if current_password==db_password:
      cursor.execute(f"update users set userPassword='{change_password}' where userId={userid}")
      cnx.commit()
      cnx.close()
      return {"message":"password is successfully changed"}, 200
    else:
      return {"message":"Current Password is not correct, Try Again!"}, 400 

  except Exception as e:
    print(e)
    print("hi")
    return {"message":"Exception occured!"},401
  
def add_user_to_db(data):
  cursor.execute(f"INSERT INTO users (userFullName, userEmailId, userPassword, userMobileNumber, userExperience) values ({data['inputFullName']}, {data['inputEmailId']}, {data['inputPassword']}, {data['inputMobileNumber']}, {data['inputExperience']})")
  result=cursor.fetchall()
  print(result)
  cnx.commit()
  print("data inserted successfully")

'''
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




def add_user_to_db(data):
  with engine.connect() as conn:
    statement = text(
      "INSERT INTO users (userFullName, userEmailId, userPassword, userMobileNumber, userExperience) values (:userFullName, :userEmailId, :userPassword, :userMobileNumber, :userExperience)"
    )
    result = conn.execute(
      statement, {
        "userFullName": data['inputFullName'],
        "userEmailId": data['inputEmailId'],
        "userPassword": data['inputPassword'],
        "userMobileNumber": data['inputMobileNumber'],
        "userExperience": data['inputExperience']
      })
    conn.commit()
  print("data inserted successfully")


def get_password_for_user(username):
  try:
      with engine.connect() as conn:
        statement = text("select userPassword, userFullName from users where userEmailId = :username")
        result = conn.execute(statement, {"username":username})
        final_result = result.fetchone()
        print(f"final result, {final_result[0]}")
        return final_result[0], final_result[1], 200
      
  except Exception as e:
    print(f"User doesn't exist")
    return {"message":"User Not Found!"}, 404




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
    conn.commit()
  print("data inserted successfully")

def select_row_from_db(jod_id):
  with engine.connect() as conn:
    select_statement = text("SELECT * FROM applications WHERE job_id = :job_id")
    select_result = conn.execute(select_statement, {"job_id": jod_id})
    inserted_data = select_result.fetchone()
    print("Inserted data:", inserted_data)

#create a function that fetchs a rows from the applications table for specific id
def fetch_rows_from_db(id):
  with engine.connect() as conn:
    select_statement = text("SELECT * FROM applications WHERE id = :id")
    select_result = conn.execute(select_statement, {"id": id})
    inserted_data = select_result.fetchall()
    print("application data:", inserted_data)
    #return inserted_data as a list of dictionaries
    return [dict(zip(select_result.keys(), row)) for row in inserted_data]

#select_row_from_db(1)
#fetch_rows_from_db(14)
# get_password_for_user("kumargaurav1527@gil.com")
check_password("gaurav")
'''
# print(load_job_from_db(1))
test_data = {
    'inputFullName': 'John Doe',
    'inputEmailId': 'john@example.com',
    'inputPassword': 'secretpassword',
    'inputMobileNumber': '1234567890',
    'inputExperience': '3 years'
}

# add_user_to_db(test_data)

# get_password_for_user("kumargaurav1527@gmail.com")

change_password_for_user(8,"test","test1")