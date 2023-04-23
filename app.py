from flask import Flask, render_template, request, redirect, session, url_for, jsonify
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
    ssl={'ssl_ca': '/etc/ssl/cert.pem'},
    cursorclass=pymysql.cursors.
    DictCursor  #to convert cursor data to dictionary
)


def getMysql():
    return pymysql.connect(
        host='aws.connect.psdb.cloud',
        user=os.getenv('your_username'),
        password=os.getenv('your_password'),
        db='acts',
        ssl={'ssl_ca': '/etc/ssl/cert.pem'},
        cursorclass=pymysql.cursors.
        DictCursor  #to convert cursor data to dictionary
    )


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


#########################################################################################


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
            cursor.execute(
                'SELECT * FROM userregister WHERE user_id = %s AND password = %s ',
                (user_id, password))
            account = cursor.fetchone()
            if account:  # If the account exists
                # Creating session variables to track the user's login status
                session['loggedin'] = True
                session['user_id'] = account['user_id']
                session['password'] = account['password']
                return redirect(
                    'userhome'
                )  # Redirecting to the index page with a success message
            if not account:  # If the account does not exist
                msg = 'Incorrect username / password!'
                return render_template('user/user_login.html', msg=msg)
    return render_template('user/user_login.html')


#user home
@app.route("/userhome")
def user_home():
    with mysql.cursor() as cursor:
        cursor.execute("SELECT * FROM bloodpublish")
        data = cursor.fetchall()
    if 'user_id' in session:
        return render_template('user/user_home.html', bloodrequestdata=data)
    else:
        return redirect(url_for('userlogin'))


#user registration
@app.route("/userregister")
def userregister():
    return render_template('user/userregister.html')


#user registration backend
@app.route("/userregisterbackend", methods=['GET', 'POST'])
def userregisterbackend():
    if request.method == 'POST':
        # Retrieving username and password from the login form
        name = request.form['name']
        phone = int(request.form['phone'])
        user_id = request.form['user_id']
        email = request.form['email']
        password = request.form['password']
        print(name)
        with mysql.cursor() as cursor:
            # Retrieving account details from the database if the username and password match
            cursor.execute(
                'INSERT INTO userregister VALUES (%s, %s, %s, %s, %s )',
                (name, phone, user_id, email, password))
            mysql.commit()
            return render_template('user/user_login.html')


########################################################################################
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
            cursor.execute(
                'SELECT * FROM driverregister WHERE driver_id = %s AND password = %s ',
                (driver_id, password))
            account = cursor.fetchone()
            if account:  # If the account exists
                # Creating session variables to track the driver's login status
                session['loggedin'] = True
                session['driver_id'] = account['driver_id']
                session['password'] = account['password']
                return redirect(
                    'driverhome'
                )  # Redirecting to the index page with a success message
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


#driver registration
@app.route("/driverregister")
def driverregister():
    return render_template('driver/driverregister.html')


#driver registration backend
@app.route("/driverregisterbackend", methods=['GET', 'POST'])
def driverregisterbackend():
    if request.method == 'POST':
        driver_id = request.form['driver_id']
        password = int(request.form['password'])
        driver_name = request.form['driver_name']
        phone = int(request.form['phone'])
        print(driver_name)
        with mysql.cursor() as cursor:

            cursor.execute(
                'INSERT INTO driverregister VALUES (%s, %s, %s, %s )',
                (driver_id, password, driver_name, phone))
            mysql.commit()
            return render_template('driver/driver_login.html')


#accident detail
@app.route("/accidentdetail")
def accidentdetail():
    return render_template('driver/accidentdetail.html')


#user registration backend
@app.route("/accidentdetailbackend", methods=['GET', 'POST'])
def accidentdetailbackend():
    if request.method == 'POST':
        # Retrieving username and password from the login form
        actsid = request.form['actsid']
        name = 'null'
        location = request.form['location']
        noofpeople = int(request.form['noofpeople'])
        veh_accident = request.form['veh_accident']
        hospname = request.form['hospname']
        address = request.form['address']
        date = datetime.now()
        time = str(datetime.today().strftime("%I:%M %p"))
        station = 'null'
        with mysql.cursor() as cursor:
            # Retrieving account details from the database if the username and password match
            cursor.execute(
                'INSERT INTO  accidentdetail VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)',
                (actsid, name, location, noofpeople, veh_accident, hospname,
                 address, date, time, station))
            mysql.commit()
            return render_template('driver/driver_home.html')


########################################################################################


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
            cursor.execute(
                'SELECT * FROM hospitalregister WHERE hospital_id = %s AND password = %s ',
                (hospital_id, password))
            account = cursor.fetchone()
            if account:  # If the account exists
                # Creating session variables to track the user's login status
                session['loggedin'] = True
                session['hospital_id'] = account['hospital_id']
                session['password'] = account['password']
                return redirect(
                    'hospitalhome'
                )  # Redirecting to the index page with a success message
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


#hospital registration
@app.route("/hospitalregister")
def hospitalregister():
    return render_template('hospital/hospitalregister.html')


#hospital registration backend
@app.route("/hospitalregisterbackend", methods=['GET', 'POST'])
def hospitalregisterbackend():
    if request.method == 'POST':

        hospital_id = request.form['hospital_id']
        hname = request.form['hname']
        hphone = int(request.form['hphone'])
        hospital_location = request.form['hospital_location']
        hospital_latitude = float(request.form['hospital_latitude'])
        hospital_longitude = float(request.form['hospital_longitude'])
        password = (request.form['password'])
        with mysql.cursor() as cursor:

            cursor.execute(
                'INSERT INTO hospitalregister VALUES (%s, %s, %s, %s,%s,%s,%s )',
                (hospital_id, hname, hphone, hospital_location,
                 hospital_latitude, hospital_longitude, password))
            mysql.commit()
            return render_template('hospital/hospital_login.html')


#blood donator list
@app.route("/bloodonatorlist")
def bloodonatorlist():
    with mysql.cursor() as cursor:
        cursor.execute("SELECT * FROM userblooddonation")
        data = cursor.fetchall()
        return render_template('hospital/bloodonatorlist.html',
                               blooddonatordata=data)


#blood request list
@app.route("/bloodrequestlist")
def bloodrequestlist():
    with mysql.cursor() as cursor:
        cursor.execute("SELECT * FROM bloodpublish")
        data = cursor.fetchall()
        return render_template('hospital/bloodrequestlist.html',
                               bloodrequestdata=data)


########################################################################################


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
            cursor.execute(
                'SELECT * FROM adminregister WHERE admin_id = %s AND password = %s ',
                (admin_id, password))
            account = cursor.fetchone()
            if account:  # If the account exists
                # Creating session variables to track the user's login status
                session['loggedin'] = True
                session['admin_id'] = account['admin_id']
                session['password'] = account['password']
                return redirect(
                    'adminhome'
                )  # Redirecting to the index page with a success message
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


#accident list
@app.route("/accidentlist")
def accidentlist():
    with mysql.cursor() as cursor:
        cursor.execute("SELECT * FROM accidentdetail")
        data = cursor.fetchall()
        return render_template('admin/accidentlist.html', accidentdata=data)


#driver list
@app.route("/driverlist")
def driverlist():
    with mysql.cursor() as cursor:
        cursor.execute("SELECT * FROM driverregister")
        data = cursor.fetchall()
        return render_template('admin/driverlist.html', driverdata=data)


#hospital list
@app.route("/hospitallist")
def hospitallist():
    with mysql.cursor() as cursor:
        cursor.execute("SELECT * FROM hospital")
        data = cursor.fetchall()
        return render_template('admin/hospitallist.html', hospitaldata=data)


############################################################################################


#blood donation for users for uploading the details
@app.route("/userbloodonation", methods=['GET', 'POST'])
def userbloodonation():
    return render_template('user/userbloodonation.html')


#blood donation backend for inserting into database
@app.route("/userbloodonationbackend", methods=['GET', 'POST'])
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
            cursor.execute(
                'INSERT INTO userblooddonation VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s )',
                (userid, name, dob, blood_group, ph_no, take_meds, address,
                 donated, currdate))
            mysql.commit()
            return render_template('user/user_home.html')


########################################################################################


#blood request for users  for uploading the details
@app.route("/userbloodrequest", methods=['GET', 'POST'])
def userbloodrequest():
    return render_template('user/userbloodrequest.html')


#blood request backend for inserting into database
@app.route("/userbloodrequestbackend", methods=['GET', 'POST'])
def userbloodrequestbackend():
    if request.method == 'POST':

        name = request.form['name']
        case = request.form['case']
        location = request.form['location']
        hospital = request.form['hospital']
        blood_group = request.form['blood_group']
        date = request.form['date']
        bystander_name = request.form['bystander_name']
        bystander_ph = request.form['bystander_ph']
        other = request.form['other']

        print(name)
        with mysql.cursor() as cursor:
            # Retrieving account details from the database if the username and password match
            cursor.execute(
                'INSERT INTO bloodpublish VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s )',
                (name, case, location, hospital, blood_group, date,
                 bystander_name, bystander_ph, other))
            mysql.commit()
            return render_template('user/user_home.html')

    #################################################################################


#blood request for hospitals  for uploading the details
@app.route("/hospitalbloodrequest")
def hospitalbloodrequest():
    return render_template('hospital/hospitalbloodrequest.html')


#blood request backend for inserting into database
@app.route("/hospitalbloodrequestbackend", methods=['GET', 'POST'])
def hospitalbloodrequestbackend():
    if request.method == 'POST':

        name = request.form['name']
        case = request.form['case']
        location = request.form['location']
        hospital = request.form['hospital']
        blood_group = request.form['blood_group']
        date = request.form['date']
        bystander_name = request.form['bystander_name']
        bystander_ph = request.form['bystander_ph']
        other = request.form['other']

        print(name)
        with mysql.cursor() as cursor:
            # Retrieving account details from the database if the username and password match
            cursor.execute(
                'INSERT INTO bloodpublish VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s )',
                (name, case, location, hospital, blood_group, date,
                 bystander_name, bystander_ph, other))
            mysql.commit()
            return render_template('hospital/hospital_home.html')

    #################################################################################


################################ Notification Section ##################################################
@app.route('/accidentSendNotify')
def accidentSendNotify():
    return render_template('user/accidentSendNotify.html')


#sending notification to accident notify
@app.route("/accidentNotify", methods=['POST'])
def accidentNotify():
    lat = request.form['latitude']
    long = request.form['longitude']
    loc = request.form['location']
    mysql = getMysql()
    with mysql.cursor() as cursor:
        cursor.execute(
            "INSERT INTO accident_notify(latitude, longitude, location) VALUES (%s, %s, %s)",
            (lat, long, loc))
        mysql.commit()
    data = {'id': cursor.lastrowid}
    return jsonify(data)


#getting live location from driver
@app.route('/accidentDriver/<int:id>', methods=['GET'])
def accidentDriver(id):
    mysql = getMysql()
    with mysql.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM accident_notify WHERE id=%s AND driver_id is NOT NULL",
            (id))
        data = cursor.fetchone()

        if not data:
            return jsonify([])

        cursor.execute("SELECT * FROM driverlocation WHERE driver_id=%s",
                       (data['driver_id']))
        driver_location = cursor.fetchone()
        return jsonify(driver_location)


#live location for driver
@app.route('/liveLocation', methods=['POST'])
def liveLocation():
    driver_id = session['driver_id']
    mysql = getMysql()
    with mysql.cursor() as cursor:
        lat = request.form['latitude']
        long = request.form['longitude']
        loc = request.form['location']
        sql = "UPDATE driverlocation SET latitude=%s, longitude=%s, locationName=%s, timestamp=CURRENT_TIME() WHERE driver_id=%s"
        cursor.execute(sql, (lat, long, loc, driver_id))
        mysql.commit()
        return str(driver_id)


#getting driver id FROM IT
@app.route('/accidentNotification', methods=['GET', 'POST'])
def accidentNotification():
    last_id = request.args.get('last_id')
    mysql = getMysql()
    with mysql.cursor() as cursor:
        sql = "SELECT * FROM accident_notify WHERE id > %s AND driver_id IS NULL AND timestamp >= DATE_SUB(NOW(), INTERVAL 10 MINUTE) ORDER BY id DESC"
        cursor.execute(sql, (last_id))
        data = cursor.fetchall()
    mysql.close()
    return jsonify(data)


#accept or reject of request
@app.route('/acceptReject/<int:id>', methods=['GET', 'POST'])
def acceptReject(id):
    mysql = getMysql()
    if request.method == 'POST':
        with mysql.cursor() as cursor:
            driver_id = session['driver_id']
            id = request.form['id']
            status = request.form['status']
            if status == 'accept':
                # if id = driver id no accept!!!
                sql = "UPDATE accident_notify SET driver_id = %s WHERE id = %s;"
                cursor.execute(sql, (driver_id, id))
                mysql.commit()
                return redirect("/driverhome")

            return redirect("/driverhome")
    elif request.method == 'GET':
        with mysql.cursor() as cursor:
            sql = "SELECT * FROM accident_notify WHERE id = %s AND driver_id IS NULL"
            cursor.execute(sql, (id))
            data = cursor.fetchone()
            if not data:
                return redirect("/driverhome")
            return render_template('driver/acceptReject.html',
                                   data=data,
                                   id=id)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
