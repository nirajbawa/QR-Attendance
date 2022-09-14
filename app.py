from flask import *
from flask_mail import Mail
import random
from flask_mysqldb import MySQL

defaultData = {
    "Title": "QR Attendance",
    "favicons": ["favicon_11-9-2022/apple-touch-icon.png", "favicon_11-9-2022/favicon-32x32.png", "favicon_11-9-2022/favicon-16x16.png", "favicon_11-9-2022/site.webmanifest", "favicon_11-9-2022/safari-pinned-tab.svg"],
    "layoutCss": ["layout/layout-main.css"],
    "menuItems": "",
    "layoutJs": ["layout.js"],
    "pageCss": "",
    "adminItems": "",
    "adminItemslinks": ""
}

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

serverType = params['serverType']

app = Flask(__name__)

app.secret_key = 'super-secret-key'

# flask main config

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['email'],
    MAIL_PASSWORD=params['Emailpassword']
)

mail = Mail(app)

# mysql config

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'qrattendance'


mysql = MySQL(app)


@app.route('/')
def home():
    if "user" in session:
        return redirect(url_for("admin"))
    else:
        homedata = {
            "homeJs": ["js/home.js"]
        }
        defaultData["pageCss"] = ["home/home-main.css"]
        defaultData["adminItems"] = ""
        defaultData["adminItemslinks"] = ""
        defaultData["menuItems"] = ["sign in", "sign up"]
        return render_template("home.html", data=defaultData, homedata=homedata)


@app.route('/sign-in', methods=['GET', 'POST'])
def signIn():
    if (request.method == 'POST'):
        userEmail = request.json['email']
        print(userEmail)
        try:
            cur = mysql.connection.cursor()
            print("r")
            cur.execute(
                '''select email from users where email = %s;''', [userEmail])
            numofrow = cur.fetchall()
            print(len(numofrow))
            mysql.connection.commit()
            cur.close()
            if (len(numofrow) != 0):
                otp = random.randint(1000, 1000000)
                mail.send_message('New Message Send From QR Attendance',
                                  sender=params["email"],
                                  recipients=[userEmail],
                                  body="OTP : " + str(otp)
                                  )
                session['SOTP'] = otp
                session['Semail'] = userEmail
                return jsonify({"status": "OTP Is Sent On your Email Please Check Your Inbox",
                                "code": "0",
                                })
            else:
                return jsonify({"status": "Eamil Is Not Register With Us please Create Account First",
                                "code": "1"
                                })

        except Exception as e:
            return jsonify({"status": "failed"})
    else:
        return jsonify({"status": "failed"})


@app.route('/sign-in-to-admin', methods=['GET', 'POST'])
def signinOtp():
    if (request.method == 'POST'):
        Uotp = request.json["otp"]
        if "SOTP" in session:
            if (str(Uotp) == str(session['SOTP'])):
                session["user"] = session['Semail']
                session.pop("Semail");
                session.pop("SOTP");
                return jsonify({"status": "sign in successfully",
                                "url": "/Admin",
                                "code": "0"
                                })
            else:
                return jsonify({"status": "Please Enter valid OTP",
                                "code": "1",
                                })
        else:
            return jsonify({"status": "please try again",
                            "code": "2",
                            "url": "/"
                            })
    else:
        return jsonify({"status": "failed"})


@app.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    if (request.method == 'POST'):
        email = request.json["email"]
        instname = request.json["institutename"]
        instype = request.json["institutetype"]
        otp = random.randint(1000, 1000000)

        try:
            cur = mysql.connection.cursor()
            cur.execute(
                '''select email from users where email = %s;''', [email])
            numofrow = cur.fetchall()
            print(len(numofrow))
            mysql.connection.commit()
            cur.close()

            if (len(numofrow) == 0):
                session["email"] = email
                session["institutename"] = instname
                session["institutetype"] = instype
                mail.send_message('New Message Send From QR Attendance',
                                  sender=params["email"],
                                  recipients=[session["email"]],
                                  body="OTP : " + str(otp)
                                  )
                session['cotp'] = otp
                return jsonify({"status": "OTP Sent On Your Email",
                                "code": "0"
                                })
            else:
                return jsonify({"status": "Email is Already Exist please Try Sign in",
                                "code": "1"
                                })

        except Exception as e:

            mail.send_message('New Message Send From QR Attendance',
                              sender=params["email"],
                              recipients=[session["email"]],
                              body="OTP : " + str(otp)
                              )
            session['cotp'] = otp
            return jsonify({"status": "success",
                            "code": "0"
                            })


@app.route('/createAccout', methods=['GET', 'POST'])
def createAccout():
    if (request.method == 'POST'):
        caotp = request.json["signupotp"]
        print(caotp)
        print(session['cotp'])
        if (str(caotp) == str(session['cotp'])):
            email = session["email"]
            instName = session["institutename"]
            insttype = session["institutetype"]

            try:
                cursor = mysql.connection.cursor()
                cursor.execute(
                    ''' INSERT INTO users (email, institutename, institutetype) VALUES(%s, %s, %s);''', (email, instName, insttype))
                mysql.connection.commit()
                cursor.close()
                session.pop("cotp")
                session["user"] = email
                session.pop("email")
                session.pop("institutename")
                session.pop("institutetype")

                return jsonify({"status": "Accout created successfully",
                                "code": "0",
                                "url": "/Admin"
                                })

            except Exception as e:
                cursor = mysql.connection.cursor()
                cursor.execute(
                    '''create table users (id int primary key not null, email text (100) not null, institutename text (100) not null, institutetype text (100) not null);''')
                cursor.execute(
                    ''' INSERT INTO users VALUES(%s,%s,%s, %s);''', (1, email, instName, insttype))
                mysql.connection.commit()
                cursor.close()
                session.pop("cotp")
                session["user"] = email
                session.pop("email")
                session.pop("institutename")
                session.pop("institutetype")

                return jsonify({"status": "Accout created successfully",
                                "code": "0",
                                "url": "/Admin"
                                })

        else:
            return jsonify({"status": "Please Enter Valid OTP",
                            "code": "1"
                            })

@app.route('/signout', methods=['GET'])
def signout():
    if("user" in session):
        session.pop("user")
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))
    
    
    
@app.route('/Admin')
def admin():
    if "user" in session:
        defaultData["pageCss"] = ["admin/admin-main.css"]
        defaultData["menuItems"] = ""
        defaultData["adminItems"] = ["home", "signout"]
        defaultData["adminItemslinks"] = ["/Admin", "/signout"]
        return render_template("admin.html", data=defaultData)
    else:
        return redirect(url_for('home'))
    
@app.route('/Admin/creare-new-batch')
def createNewBatch


if __name__ == "__main__":
    app.run(debug=True)
