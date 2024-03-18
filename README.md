# AWS-Project

Step-01: Setup an RDS in AWS

ENDPOINT="rdsdb.cepeyk3wjm1v.us-east-1.rds.amazonaws.com"

PORT="3306"

USR="admin"

PASSWORD="abcd1234"

DBNAME="rdsdb"

&nbsp;

Step-02: Setup an S3 bucket

Bucket name: s3bucketmaddela

ARN: arn:aws:s3:::s3bucketmaddela

Account ID: 6xxxxxxxxxx3


Step-03: An SNSTopic will be created using boto3 in app.py


Step-04: Lambda function will be created using boto3 in app.py


Step-05: Create a simple ‘register.html’ page
It will take the entered email address and password, compare it with existing users in the table ‘userdetails’. If the user is not already present, it will add user. If the user is added to the table, you will be redirected to the ‘login.html’ page. Else, you will be redirected back to the ‘register.html’ page. 
Alternatively, if you have registered already, you can click on ‘Are you already a registered user?’ to skip to the ‘login.html’ page.

![image](https://github.com/maddies-codespace/AWS-Project/assets/141537679/504b46c7-ad62-4ffd-875e-1ef6933f9a48)

Step-06: Create a 'login.html' page
Enter login credentials here. Your details will be checked in the ‘userdetails’ table and if there is a match, you will be redirected to the ‘upload.html’ page. If your credentials don’t match, you will be redirected to the ‘register.html’ page. 

![image](https://github.com/maddies-codespace/AWS-Project/assets/141537679/d646a7e9-c998-40ab-b6c5-d8582789a84d)

Up to 5 e-mail addresses that need to be notified of a file upload can be entered here. The file will be uploaded to the above mentioned s3 bucket.

![image](https://github.com/maddies-codespace/AWS-Project/assets/141537679/edf1837e-2b86-486d-a6a2-fb71db0039d8)

The goal is to setup an s3bucket that can have files uploaded to it by registered users. The user will decide which email addresses to notify, they will recieve a notification to download the file from the s3bucket. When a file is uploaded, a new subscription topic will be created using boto3 in app.py. These email addresses will each be added to the topic and confirmation request emails will be sent out. The file uploaded to the page will be uploaded to the s3 bucket which will trigger a lambda event to send an email to the above email addresses with the arn for the file. Additionally, the rds table, ‘useractivity’ will be updated with the email address of the uploader, filename, the arn for the uploaded file, the 5 email addresses, etc.

The video below explains the process in greater detail.

[![Watch the video](https://img.youtube.com/vi/UZEnUoBTggs/hqdefault.jpg)](https://www.youtube.com/embed/UZEnUoBTggs)

<!---
([<img src="https://img.youtube.com/vi/UZEnUoBTggs/hqdefault.jpg" width="600" height="300"
/>](https://www.youtube.com/embed/UZEnUoBTggs))
-->
