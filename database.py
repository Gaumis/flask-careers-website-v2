import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
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

#return [dict(zip(select_result.keys(), row)) for row in inserted_data]

def get_candidate_details_with_jobs(application_id):
  with engine.connect() as conn:
    statement = text("SELECT app.id, app.job_id ,j.title, j.location, app.full_name, app.linkedin_url, app.education, app.work_experience, app.resume_url, app.status FROM applications app JOIN jobs j ON app.job_id = j.id where app.id=:application_id")
    result = conn.execute(statement, {"application_id": application_id})
    final_result = result.fetchall()
    print(final_result)
    print(f"Result is : {result.keys}")
    if final_result:
      return [dict(zip(result.keys(),row)) for row in final_result]
    else:
      return None


def take_action_db(app_id,status):
  try:
    with engine.connect() as conn:
      statement = text("update applications set status=:status where id=:app_id")
      result = conn.execute(statement, {"status": status,
                                        "app_id":app_id})
      conn.commit()
    return {"message": "Application status is successfully changed"}, 200
  except Exception as e:
    print(f"Database error: {e}")
    return {"error": "Failed to update application status"}, 500
  

def load_job_application(job_id, application_id):
  with engine.connect() as conn:
    statement = text("select * from applications app JOIN jobs j ON app.job_id=j.id where app.id=:application_id and j.id=:job_id")
    result = conn.execute(statement, {"application_id":application_id,
                                      "job_id":job_id})
    final_result=result.fetchall()
    print(result.keys)
    if final_result:
      return dict(zip(result.keys(),final_result))
    else:
      return None

def check_user_in_db(userEmail):
  with engine.connect() as conn:
    statement = text(
      "select userId from users where userEmailId = :userEmail"
    )
    result = conn.execute(statement, {"userEmail":userEmail})
    final_result=result.fetchall()
    userExist=len(final_result)
    if userExist == 0:
      return True
    else:
      return False


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


def change_password_for_user(userid, current_password, change_password):
  print("entered change password database")
  try:
    with engine.connect() as conn:
      statement = text(
      "select userPassword from users where userId = :userid"
      )
      result = conn.execute(statement, {"userid":userid})
      final_result = result.fetchall()
      print(f"final result is {final_result}")
      db_password=final_result[0][0]
      print(f"password is : {db_password}")
      if current_password==db_password:
        print("current password and db password is same")
        statement = text(
          "update users set userPassword = :change_password where userId = :userid"
        )
        result = conn.execute(statement, {"userid":userid, "change_password":change_password})
        print("current password and db password is close")
        conn.commit()
        conn.close()
        return {"message":"password is successfully changed"}, 200
      else:
        return {"message":"Current Password is not correct, Try Again!"}, 400
      
  except Exception as e:
    return {"message":"Exception occured!"},401

def db_get_all_application(id):
  try:
    with engine.connect() as conn:
      statement = text("select * from applications where job_id = :id")
      result = conn.execute(statement, {"id": id})
      final_result = result.fetchall()
      print(f"{final_result} and type is {type(final_result)}")
      return [dict(zip(result.keys(), row)) for row in final_result]

  except Exception as e:
    print(e)
    return {"message":f"No Applications found with job id {id}"}

def get_password_for_user(username):
  try:
    with engine.connect() as conn:
      statement = text("select userPassword, userFullName, userId, role from users where userEmailId = :username")
      result = conn.execute(statement, {"username":username})
      final_result = result.fetchone()
      print(final_result)
      print(f"final result, {final_result[0]}")
      return final_result[0], final_result[1], final_result[2], final_result[3], 200
      
  except Exception as e:
    print(f"User doesn't exist")
    return {"message":"User Not Found!"}, 404

def check_if_already_applied(id, userEmail):
  with engine.connect() as conn:
    statement = text(
      "select id from applications where job_id = :id and email = :userEmail"
    )
    result = conn.execute(
      statement, {"id":id,
                  "userEmail":userEmail}
    )
    final_result = result.fetchall()
    userExist=len(final_result)
    print(userExist)
    if userExist:
      return False
    else:
      return True

def get_applied_applications(userEmail):
  with engine.connect() as conn:
    statement = text(
      "SELECT j.title, j.location, j.salary, j.currency, app.created_at, app.status FROM applications app JOIN jobs j ON app.job_id = j.id where app.email=:userEmail"
    )
    result = conn.execute(
      statement, {"userEmail":userEmail}
    )
    final_result = result.fetchall()
    print(f"Final result : {final_result}")
    if final_result:
      return final_result
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
  
# get_password_for_user("kumargaurav1527@gmail.com")
# change_password_for_user(1,"password4","password5")

#select_row_from_db(1)
#fetch_rows_from_db(14)
# get_password_for_user("kumargaurav1527@gil.com")
# check_password("gaurav")
# check_user_in_db("kumargaurav1527@gl.com")
# check_if_already_applied(2, 'bimladevi@gmail.com')
# get_applied_applications('bimladevi@gmail.com')
# ans = db_get_all_application(1)
# print(f"Answer is {ans} and the type is {type(ans)}")
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


change_password_for_user(8,"test","test1")'''
# print(get_candidate_details_with_jobs(101))
# print(load_job_application(5,101))
# print(fetch_rows_from_db(101))
take_action_db(119, 'Interviewed')