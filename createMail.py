import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Connect to SMTP server and send email
smtp_server = 'us2.smtp.mailhostbox.com'
smtp_port = 587
smtp_username = os.getenv('email')
smtp_password = os.getenv('mailpass')



def sendMail(actsid,name,location,noofpeople,veh_accident,hospname,address,date,time,getmail):
    # Define email contents
    sender = os.getenv('email')
    receiver = getmail
    subject = 'Subject of the email'
    body = 'Body of the email'
    
    body_html = body_html = f'''
<html>
    <head>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    </head>
    <body>

    <div class="card" style="width: 18rem;">
  <div class="card-body">
     
    <p class="card-text">ACTS ID: {actsid} </p>
<p class="card-text">Name: {name} </p>
<p class="card-text">Location: {location} </p>
<p class="card-text">No. of People: {noofpeople}</p>
<p class="card-text">Vehicle Involved: {veh_accident}</p>
<p class="card-text">Hospital Name: {hospname}</p>
<p class="card-text">Date: {date}</p>
<p class="card-text">Time: {time} </p>
     
  </div>
</div>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
    </body>
</html>
'''
    
    # Create message object
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['Subject'] = subject
    
    # Attach body to message object
    msg.attach(MIMEText(body, 'plain'))
    # Attach HTML part
    html_part = MIMEText(body_html, 'html')
    msg.attach(html_part)
    
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        msg['To'] = receiver
        server.sendmail(sender, receiver, msg.as_string())