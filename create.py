#!flask/bin/python
from flask import Flask
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="very_strong_password",
  database="interview_scheduler",
  auth_plugin="mysql_native_password"
)

mycursor = mydb.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/new_interview',methods=['POST', 'GET'])
def new_interview(interviewer, interviewee, start, end, date):


    mycursor.execute("SELECT * FROM interview")

    myresult = mycursor.fetchall()

    flag=0
    for x in myresult:
      if ((interviewer==x.interviewer_id or interviewee==x.interviewee_id) and date==x.interview_date and ((start>=x.start_time and start<=x.end_time ) or (end>=x.start_time and end<=x.end_time ))):
          flag=1
          print(x)

    if flag==1:
        return "error"
    else:
        mycursor.execute("""INSERT INTO interview (name,start_time,end_time) VALUES (?,?,?)""",(name,start,end))
        mydb.commit()
        return "record inserted."

@app.route('/edit_interview',methods=['POST', 'GET'])
def edit_interview(interview_id):
    mycursor.execute("SELECT * FROM interview")

    myresult = mycursor.fetchall()
    for x in myresult:
        return x



@app.route('/submit_edit_interview',methods=['POST', 'GET'])
def submit_edit_interview(interview_id,):


    mycursor.execute("SELECT * FROM interview")

    myresult = mycursor.fetchall()

    flag=0
    for x in myresult:
      if ((interviewer==x.interviewer_id or interviewee==x.interviewee_id) and date==x.interview_date and ((start>=x.start_time and start<=x.end_time ) or (end>=x.start_time and end<=x.end_time ))):
          flag=1
          print(x)

    if flag==1:
        return "error"
    else:
        mycursor.execute("""INSERT INTO interview (name,start_time,end_time) VALUES (?,?,?)""",(name,start,end))
        mydb.commit()
        return "record inserted."

@app.route('/delete_interview',methods=['POST', 'GET'])
def delete_interview(interview_id):
    sql = "DELETE FROM interview WHERE id == '%d'" % (interview_id)

    try:
       cursor.execute(sql)
       mydb.commit()
    except:
       mydb.rollback()


if __name__ == '__main__':
    app.run(debug=True)