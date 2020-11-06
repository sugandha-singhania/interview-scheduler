#!flask/bin/python
from flask import Flask, request, jsonify, render_template
import mysql.connector
from email import mime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
# import encoders
import smtplib,email,email.encoders,email.mime.text,email.mime.base

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="very_strong_password",
  database="interview_scheduler",
  auth_plugin="mysql_native_password"
)

mycursor = mydb.cursor()

app = Flask(__name__)

@app.route('/dummy',methods=['POST', 'GET'])
def dummy():
    print("sfkjsjgndjl")
    return "hi"


@app.route('/')
def index():
  return render_template("home.html")


@app.route('/new_interview',methods=['POST', 'GET'])
def new_interview():

    json_data = request.json
    interviewer_name = json_data["interviewer_name"]
    interviewee_name = json_data["interviewee_name"]
    interviewer_email = json_data["interviewer_email"]
    interviewee_email = json_data["interviewee_email"]
    date = json_data["interview_date"]
    start= json_data["start_time"]
    end = json_data["end_time"]


    mycursor.execute("SELECT * FROM interview")

    myresult = mycursor.fetchall()

    flag=0
    for x in myresult:
      if ((interviewer_email==x[6] or interviewee_email==x[7]) and date==x[3] and ((start>=x[4] and start<=x[5] ) or (end>=x[4] and end<=x[5] ))):
          flag=1
          print(x)

    if flag==1:
        return "error"
    else:
        mycursor.execute("""INSERT INTO interview (interviewer_name, interviewee_name, interviewer_email, interviewee_email ,interview_date, start_time,end_time) VALUES (%s, %s, %s, %s, %s, %s, %s)""",(interviewer_name, interviewee_name, interviewer_email, interviewee_email , date, start, end ))
        mydb.commit()
        return "record inserted."

@app.route('/edit_interview',methods=['POST', 'GET'])
def edit_interview():
    json_data = request.json
    interview_id = json_data["interview_id"]
    sql = "SELECT *  FROM interview WHERE id ='%d'" % (interview_id)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        return jsonify(x)

@app.route('/submit_edit_interview',methods=['POST', 'GET'])
def submit_edit_interview():
    json_data = request.json
    interviewer_name = json_data["interviewer_name"]
    interviewee_name = json_data["interviewee_name"]
    interviewer_email = json_data["interviewer_email"]
    interviewee_email = json_data["interviewee_email"]
    date = json_data["interview_date"]
    start= json_data["start_time"]
    end = json_data["end_time"]
    interview_id=json_data["interview_id"]

    mycursor.execute("SELECT * FROM interview")
    myresult = mycursor.fetchall()

    flag=0
    for x in myresult:
        if interview_id!=x[0]:
            if ((interviewer_email==x[6] or interviewee_email==x[7]) and date==x[3] and ((start>=x[4] and start<=x[5] ) or (end>=x[4] and end<=x[5] ))):
                flag=1
                print(x)

    if flag==1:
        return "error"
    else:
        mycursor.execute("UPDATE interview set interviewer_name = %s, interviewee_name = %s, interviewer_email = %s, interviewee_email = %s ,interview_date = %s, start_time = %s, end_time = %s where id= %s", (interviewer_name, interviewee_name, interviewer_email, interviewee_email , date, start, end, interview_id));
        mydb.commit()
        return "record inserted."

@app.route('/delete_interview',methods=['POST', 'GET'])
def delete_interview():
    json_data = request.json
    interview_id = json_data["interview_id"]
    sql = "DELETE FROM interview WHERE id ='%d'" % (interview_id)
    mycursor.execute(sql)
    mydb.commit()
    return "deleted"


def send_an_email(recipient,data):

    fromaddr = "prakash.sanchi@gmail.com"
    password= "bhdgsacvayu"
    toaddr = recipient

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "interview"
    body = ""

    msg.attach(MIMEText(body, 'plain'))
    print(msg)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
    dict  = {'response': "true" }
    return jsonify(dict)

# send_an_email("prakash.sanchi1998@gmail.com","hello")

if __name__ == '__main__':
    app.run(debug=True)
