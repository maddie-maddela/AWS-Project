#FinalProject BlazerID=Maddela
from flask import Flask, request, render_template, redirect, url_for
import pymysql
import boto3
import datetime
from werkzeug.utils import secure_filename
import time
import json

#emaillist = ["" for x in range(5)]

#Credentials for RDS
ENDPOINT="rdsdb.cepeyk3wjm1v.us-east-1.rds.amazonaws.com"
PORT="3306"
USR="admin"
PASSWORD="abcd1234"
DBNAME="rdsdb"

app = Flask(__name__)

#Credentials for S3/SNS/Lambda
S3_BUCKET = "s3bucketmaddela"
AWS_ACCESS_KEY = "AKIAY6XNQBT4Z3C24YQN"
AWS_SECRET_KEY = "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"
AWS_REGION = 'us-east-1'

#RDS connection establishment
conn =  pymysql.connect(host=ENDPOINT, user=USR, password=PASSWORD, database=DBNAME)
cur = conn.cursor()
#cur.execute("CREATE TABLE useractivity(email VARCHAR(20), password VARCHAR(20), timestamp VARCHAR(30), filename VARCHAR(100), file_ARN VARCHAR(100));")
#cur.execute("CREATE TABLE userdetails(email VARCHAR(20), password VARCHAR(20), timestamp VARCHAR(30));")

@app.route('/')
def my_form():
    return render_template('register.html')

@app.route("/register", methods=['POST','GET'])
def register():
    now = datetime.datetime.now()
    now_str = now.date().isoformat()#now.strftime('%Y-%m-%d %H:%M:%S')
    email = request.form["email"]
    password = request.form['password']
    print(email,password)

    #print("create success")
    if email and password:
        print("inside if statement")
        #return render_template('my-form2.html', content=email)
        cur.execute("SELECT * FROM userdetails Where email ='"+email+"' AND password = '"+password+"';")
        query_results = cur.fetchall()
        if len(query_results) == 0:
            cur.execute("INSERT INTO userdetails(email,password,timestamp) VALUES(%s, %s, %s);" , (email, password, now_str))
            cur.execute("SELECT * FROM userdetails;")
            query_results = cur.fetchall()
            print(query_results)
            print("Registration Successful! ")
            return render_template('login.html')
        

@app.route('/login', methods=['POST','GET'])
def login():
    uemail = request.form['uemail']
    upassword = request.form['upassword']
    print(uemail,upassword)
    email1 = request.form['email1']
    email2 = request.form['email2']
    email3 = request.form['email3']
    email4 = request.form['email4']
    email5 = request.form['email5']
    file = request.files['file1']
    print(email2)
    cur.execute("SELECT * FROM userdetails Where email ='"+uemail+"' AND password = '"+upassword+"';")
    query_results = cur.fetchall()
    if len(query_results) == 1:
        print("Login successful!")
        sns_client = boto3.client('sns', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY, region_name = AWS_REGION)
        topic = sns_client.create_topic(Name='SNSTopic')

        if file:    
            if email1:
                subscription1 = sns_client.subscribe(TopicArn = topic['TopicArn'], Protocol = 'email', Endpoint = email1, ReturnSubscriptionArn = True)['SubscriptionArn']
            if email2:
                subscription2 = sns_client.subscribe(TopicArn = topic['TopicArn'], Protocol = 'email', Endpoint = email2, ReturnSubscriptionArn = True)['SubscriptionArn']
            if email3:
                subscription3 = sns_client.subscribe(TopicArn = topic['TopicArn'], Protocol = 'email', Endpoint = email3, ReturnSubscriptionArn = True)['SubscriptionArn']
            if email4:
                subscription4 = sns_client.subscribe(TopicArn = topic['TopicArn'], Protocol = 'email', Endpoint = email4, ReturnSubscriptionArn = True)['SubscriptionArn']
            if email5:
                subscription5 = sns_client.subscribe(TopicArn = topic['TopicArn'], Protocol = 'email', Endpoint = email5, ReturnSubscriptionArn = True)['SubscriptionArn']
        print(subscription1)
        print(topic['TopicArn'])
        print('Email Subscription successful! ')

                 
        s3_client= boto3.client("s3",aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        if file:
            now = datetime.datetime.now()
            now_str = now.date().isoformat()#now.strftime('%Y-%m-%d %H:%M:%S')
            filename=file.filename.split("\\")[-1]
            file.save(secure_filename(filename))
            #output = send_to_s3(filename, app.config["S3_BUCKET"])
            s3_client.upload_file(filename, S3_BUCKET, filename, ExtraArgs={'GrantRead': 'uri="http://acs.amazonaws.com/groups/global/AllUsers"'})
            str_path = "https://" + S3_BUCKET + ".s3.amazonaws.com/" + filename
            cur.execute("INSERT INTO useractivity(email,password,timestamp,filename, file_ARN) VALUES(%s, %s, %s, %s, %s);" , (uemail, upassword, now_str, filename, str_path))
            cur.execute("SELECT * FROM useractivity;")
            query_results = cur.fetchall()
            print(query_results)
            print("File Upload Successful! ")



            time.sleep(60)
            payload = {filename: str_path}
            response = sns_client.publish(TargetArn=topic['TopicArn'], Message=json.dumps({'default': json.dumps(payload)}),
            MessageStructure='json')
            print(response)
            print('Email notification sent')
            #cur.execute("DROP TABLE userdetails;")
            #cur.execute("DROP TABLE useractivity;")
            return render_template('register.html')
if __name__=="__main__":
    app.run(debug=True)