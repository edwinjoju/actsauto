from flask import Flask, render_template,request, redirect, session, url_for
from datetime import datetime
import pymysql.cursors
import os

app = Flask(__name__)

app.secret_key = 'mysecert'
# this cell is to connect data base to colab

mysql = pymysql.connect(
    host='aws.connect.psdb.cloud',
    user=os.getenv('your_username'),
    password=os.getenv('your_password'),
    db='acts',
    ssl = {'ssl_ca':'/etc/ssl/cert.pem'},
    cursorclass=pymysql.cursors.DictCursor #to convert cursor data to dictionary
)

#with mysql.cursor() as cursor:
#  cursor.execute('select * from userregister') 
#  item = cursor.fetchone()
# print(item)



@app.route("/")

@app.route("/home")
def home():
	return render_template('index.html')

############################################################################################
#login for user
@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
  msg = ''  # Initializing an empty message variable
  if request.method == 'POST' and 'user_id' in request.form and 'password' in request.form:
    # Retrieving username and password from the login form
    user_id = request.form['user_id']
    password = request.form['password']
    with mysql.cursor() as cursor:
      # Retrieving account details from the database if the username and password match
      cursor.execute('SELECT * FROM userregister WHERE user_id = %s AND password = %s ',(user_id, password))
      account = cursor.fetchone()
      if account:  # If the account exists
        # Creating session variables to track the user's login status
        session['loggedin'] = True
        session['user_id'] = account['user_id']
        session['password'] = account['password']
        return redirect('userhome')  # Redirecting to the index page with a success message
      if not account:  # If the account does not exist
        msg = 'Incorrect username / password!'
        return render_template('user/user_login.html', msg=msg)
  return render_template('user/user_login.html')
	
#user home 	
@app.route("/userhome")
def user_home():
  if 'user_id' in session:
    return render_template('user/user_home.html')
  else:
     return redirect(url_for('userlogin'))

#login for driver
@app.route("/driverlogin", methods=['GET', 'POST'])
def driverlogin():
  msg = ''  # Initializing an empty message variable
  if request.method == 'POST' and 'driver_id' in request.form and 'password' in request.form:
    # Retrieving username and password from the login form
    driver_id = request.form['driver_id']
    password = request.form['password']
    with mysql.cursor() as cursor:
      # Retrieving account details from the database if the username and password match
      cursor.execute('SELECT * FROM driverregister WHERE driver_id = %s AND password = %s ',(driver_id, password))
      account = cursor.fetchone()
      if account:  # If the account exists
        # Creating session variables to track the user's login status
        session['loggedin'] = True
        session['driver_id'] = account['driver_id']
        session['password'] = account['password']
        return redirect('driverhome')  # Redirecting to the index page with a success message
      if not account:  # If the account does not exist
        msg = 'Incorrect username / password!'
        return render_template('driver/driver_login.html', msg=msg)
  return render_template('driver/driver_login.html')

#driver home
@app.route("/driverhome")
def driver_home():
  if 'driver_id' in session:
    driver_id = session['driver_id']
    return render_template('driver/driver_home.html')
  else:
     return redirect(url_for('driverlogin'))



#login for hospital
@app.route("/hospitallogin", methods=['GET', 'POST'])
def hospitallogin():
  msg = ''  # Initializing an empty message variable
  if request.method == 'POST' and 'hospital_id' in request.form and 'password' in request.form:
    # Retrieving username and password from the login form
    hospital_id = request.form['hospital_id']
    password = request.form['password']
    with mysql.cursor() as cursor:
      # Retrieving account details from the database if the username and password match
      cursor.execute('SELECT * FROM hospitalregister WHERE hospital_id = %s AND password = %s ',(hospital_id, password))
      account = cursor.fetchone()
      if account:  # If the account exists
        # Creating session variables to track the user's login status
        session['loggedin'] = True
        session['hospital_id'] = account['hospital_id']
        session['password'] = account['password']
        return redirect('hospitalhome')  # Redirecting to the index page with a success message
      if not account:  # If the account does not exist
        msg = 'Incorrect username / password!'
        return render_template('hospital/hospital_login.html', msg=msg)
  return render_template('hospital/hospital_login.html')

#hospital home
@app.route("/hospitalhome")
def hospital_home():
  if 'hospital_id' in session:
    hospital_id = session['hospital_id']
    return render_template('hospital/hospital_home.html')
  else:
     return redirect(url_for('hospitallogin'))


#login for admin
@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
  msg = ''  # Initializing an empty message variable
  if request.method == 'POST' and 'admin_id' in request.form and 'password' in request.form:
    # Retrieving username and password from the login form
    admin_id = request.form['admin_id']
    password = request.form['password']
    with mysql.cursor() as cursor:
      # Retrieving account details from the database if the username and password match
      cursor.execute('SELECT * FROM adminregister WHERE admin_id = %s AND password = %s ',(admin_id, password))
      account = cursor.fetchone()
      if account:  # If the account exists
        # Creating session variables to track the user's login status
        session['loggedin'] = True
        session['admin_id'] = account['admin_id']
        session['password'] = account['password']
        return redirect('adminhome')  # Redirecting to the index page with a success message
      if not account:  # If the account does not exist
        msg = 'Incorrect username / password!'
        return render_template('admin/admin_login.html', msg=msg)
  return render_template('admin/admin_login.html')

#admin home
@app.route("/adminhome")
def admin_home():
  if 'admin_id' in session:
    admin_id = session['admin_id']
    return render_template('admin/admin_home.html')
  else:
     return redirect(url_for('adminlogin'))
############################################################################################


#blood donation for users for uploading the details
@app.route("/userbloodonation", methods=['GET', 'POST'])
def userbloodonation():
  return render_template('user/userbloodonation.html')

#blood donation backend for inserting into database 
@app.route("/userbloodonationbackend", methods=['GET','POST'])
def userbloodonationbackend():
  if request.method == 'POST':
    # Retrieving username and password from the login form
    userid = 1
    name = request.form['name']
    dob = request.form['dob']
    take_meds = request.form['take_meds']
    donated = request.form['donated']
    blood_group = request.form['blood_group']
    address = request.form['address']
    ph_no = int(request.form['ph_no'])
    currdate = datetime.now()
    print(name)
    with mysql.cursor() as cursor:
      # Retrieving account details from the database if the username and password match
      cursor.execute( 'INSERT INTO userblooddonation VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s )',
          (userid,name,dob,blood_group,ph_no,take_meds,address,donated,currdate))
      mysql.commit()
      return render_template('user/user_home.html' )
  


if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)



#<p>{{ user.username }}</p>

     #{% for row in items %}
 #                       <tr>
  #                        <td><a href="{{ row.link}}" class="text-primary">{{row.name}}</a></td>
 #                         <td>{{ row.desc}}</td>
  #                        <td><span class="badge bg-success">Viewed</span></td>
  #                      </tr>
   #   {% endfor %}