# from flask module we are importing Flask class
from flask import Flask, render_template

# object of Flask class is created with __name__ which is equal to __main__
app = Flask(__name__)

# @ symbol is decorator 
@app.route("/")
def hello_world():
  return render_template('home.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)