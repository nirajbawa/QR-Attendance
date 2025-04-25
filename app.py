from flask import *
from flask_mail import Mail
import random
from flask_mysqldb import MySQL
import pyqrcode
import png
from pyqrcode import QRCode
import os
import json
from datetime import date, datetime
from dotenv import load_dotenv
load_dotenv()

 
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



app = Flask(__name__)

app.secret_key = 'super-secret-key'

# flask main config

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD")
)


mail = Mail(app)

# mysql config

app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")

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
                                  sender=os.getenv("MAIL_USERNAME"),
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
            return jsonify({"status": "Eamil Is Not Register With Us please Create Account First"})
    else:
        return jsonify({"status": "failed"})


@app.route('/sign-in-to-admin', methods=['GET', 'POST'])
def signinOtp():
    if (request.method == 'POST'):
        Uotp = request.json["otp"]
        if "SOTP" in session:
            if (str(Uotp) == str(session['SOTP'])):
                session["user"] = session['Semail']
                session.pop("Semail")
                session.pop("SOTP")
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
            print("hello")
            cur.execute("SELECT COUNT(email) FROM `users` WHERE email = '"+email+"';")
            numofrow = cur.fetchall()
            mysql.connection.commit()
            cur.close()

            if (numofrow[0][0] == 0):
                session["email"] = email
                session["institutename"] = instname
                session["institutetype"] = instype
                mail.send_message('New Message Send From QR Attendance',
                                  sender=os.getenv("MAIL_USERNAME"),
                                  recipients=[session["email"]],
                                  body="OTP : " + str(otp)
                                  )
                session['cotp'] = otp
                print("out"+ str(session['cotp']))
                return jsonify({"status": "OTP Sent On Your Email",
                                "code": "0"
                                })
            else:
                return jsonify({"status": "Email is Already Exist please Try Sign in",
                                "code": "1"
                                })

        except Exception as e:
            session["email"] = email
            session["institutename"] = instname
            session["institutetype"] = instype
            mail.send_message('New Message Send From QR Attendance',
                              sender=os.getenv("MAIL_USERNAME"),
                              recipients=[email],
                              body="OTP : " + str(otp)
                              )
            session['cotp'] = otp
            print("in"+ str(session['cotp']))
            return jsonify({"status": "OTP Sent On Your Email",
                                "code": "0"
                                })


@app.route('/createAccout', methods=['GET', 'POST'])
def createAccout():
    if (request.method == 'POST'):
        print("by")
        caotp = request.json["signupotp"]
        print(":::"+caotp)
        print("+++"+str(session['cotp']))
        if (str(caotp) == str(session['cotp'])):
            print("hii")
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
                print("hello")
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
    if ("user" in session):
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
        albox = {}
        if("almsg" in session):
            print("yes")
            albox = {"alboxd":"block", "alboxm": session["almsg"], "albc":session["alcode"]}
            session.pop("almsg")
            session.pop("alcode")
        else:
            albox = {"alboxd":"none", "alboxm":"", "albc":""}
        return render_template("admin.html", data=defaultData, aldata=albox)
    else:
        return redirect(url_for('home'))


@app.route('/Admin/creare-new-batch', methods=['GET', 'POST'])
def createNewBatch():
    if "user" in session:
        defaultData["pageCss"] = [
            "admin/create-new-batch/create-new-batch.css"]
        defaultData["menuItems"] = ""
        defaultData["adminItems"] = ["home", "signout"]
        defaultData["adminItemslinks"] = ["/Admin", "/signout"]

        createNewBatchdata = {
            "createNewBatchdata": ["js/create-batch.js"]
        }
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT bName, id FROM `"+session['user']+"_batchs`;")
            numofrow = cursor.fetchall()
            rowlen = len(numofrow)
            print(numofrow)
            mysql.connection.commit()
            cursor.close()
        except Exception as e:
            numofrow = ""
        return render_template("create-batch.html", data=defaultData, createNewBatchdata=createNewBatchdata, numofrow=numofrow)
    else:
        return redirect(url_for('home'))


@app.route('/Admin/batchApi', methods=['GET', 'POST'])
def createNewBatchapi():
    if (request.method == 'POST' and "user" in session):
        data = request.json["data"]
        tbname = session["user"] + "_batchs"
        bname = data["bName"]
        bsubjects = json.dumps(data["bsubjects"])
        bstime = data["CsT"]
        betime = data["CeT"]
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO `"+session['user']+"_batchs` (`id`, `bName`, `bSubjects`, `bsTime`, `beTime`, `Etime`) VALUES (NULL, '" +
                           bname+"', '"+bsubjects+"', '"+bstime+"', '"+betime+"', current_timestamp());")
            mysql.connection.commit()
            cursor.close()
            return jsonify({"status": "Account Created Successfully",
                            "code": "0"
                            })
        except Exception as e:
            # CREATE TABLE `qrattendance`.`nirajbava222@gmail.comd_batchs` (`id` INT(50) NOT NULL AUTO_INCREMENT , `bName` TEXT NOT NULL , `bSubjects` TEXT NOT NULL , `bsTime` TEXT NOT NULL , `beTime` TEXT NOT NULL , `Etime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (`id`)) ENGINE = InnoDB;
            cursor = mysql.connection.cursor()
            cursor.execute("CREATE TABLE `"+tbname+"` (`id` INT(50) NOT NULL AUTO_INCREMENT , `bName` TEXT NOT NULL , `bSubjects` TEXT NOT NULL , `bsTime` TEXT NOT NULL , `beTime` TEXT NOT NULL , `Etime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (`id`)) ENGINE = InnoDB;")
            cursor.execute("INSERT INTO `"+session['user']+"_batchs` (`id`, `bName`, `bSubjects`, `bsTime`, `beTime`, `Etime`) VALUES (1, '" +
                           bname+"', '"+bsubjects+"', '"+bstime+"', '"+betime+"', current_timestamp());")
            mysql.connection.commit()
            cursor.close()
            return jsonify({"status": "Account Created Successfully",
                            "code": "0"
                            })

    else:
        return jsonify({"status": "Try Again"})


@app.route('/Admin/addstudents/<string:id>', methods=['GET', 'POST'])
def addStudents(id):
    if ("user" in session):
        defaultData["pageCss"] = ["admin/add-students/add-students.css"]
        defaultData["menuItems"] = ""
        defaultData["adminItems"] = ["home", "signout"]
        defaultData["adminItemslinks"] = ["/Admin", "/signout"]

        addstudents = {
            "addstudentsdata": ["js/add-students.js"]
        }
        salt = {"altmsg":"", "altd":"none"}
        if("saltmsg" in session):
            salt = {"altmsg":session["saltmsg"], "altd":"block"}
            session.pop("saltmsg")
            
        print(id)
        try:

            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT * FROM `"+session['user']+"_students` WHERE bid = "+id+";")
            rows = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
        
        except Exception as e:
            rows = ""
        return render_template("add-students.html", data=defaultData, addstudents=addstudents, rows=rows, batchid = str(id), saltdata = salt)
    else:
        return ("/")
    

@app.route('/Admin/addNS/', methods=['GET', 'POST'])
def addNS():
    if ("user" in session and request.method == 'POST'):    
        
        name = request.form.get("sname")
        email = request.form.get("semail")
        id = request.form.get("bid")
        rollno = request.form.get("rollno")
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO `"+session['user']+"_students` (`sid`, `bid`, `name`, `email`, `EdateT`) VALUES ("+rollno+", "+id+", '"+name+"', '"+email+"', current_timestamp());")
            mysql.connection.commit()
            cursor.close()
            return redirect("/Admin/addstudents/"+str(id))
        except Exception as e:
            try:
                cursor = mysql.connection.cursor()
                cursor.execute("CREATE TABLE `"+session['user']+"_students` (`sid` INT NOT NULL, `bid` INT(100) NOT NULL , `name` TEXT NOT NULL , `email` TEXT NOT NULL , `EdateT` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (`sid`)) ENGINE = InnoDB;")
                cursor.execute("INSERT INTO `"+session['user']+"_students` (`sid`, `bid`, `name`, `email`, `EdateT`) VALUES ("+rollno+", "+id+", '"+name+"', '"+email+"', current_timestamp());")
                mysql.connection.commit()
                cursor.close()
                return redirect("/Admin/addstudents/"+str(id))
            except Exception as e:
                session["saltmsg"] = "Please enter valid student information and make sure your Roll No is unique..."
                return redirect("/Admin/addstudents/"+str(id))
    else:
        return redirect("/")


@app.route('/Admin/qrdown/<string:bid>/<string:sid>/<string:eid>', methods=['GET', 'POST'])
def qrdownload(bid,sid,eid):
    if ("user" in session):
        s = 'http://127.0.0.1:5000/Admin/scanner/'+bid+'/'+sid+'/'+session["user"]
        # Generate QR code
        url = pyqrcode.create(s)
        otp = random.randint(1000, 1000000)
        # Create and save the svg file naming "myqr.svg"
        abspath  = os.path.abspath(os.getcwd())
        durl = os.path.join(abspath+"\\static\\images\\qrcodes\\myqr_"+str(otp)+"_"+sid+"_"+bid+".png")
        url.png(durl, scale = 6)
        return send_file(durl, as_attachment=True)
    else:
        return redirect("/")
        
@app.route('/Admin/records/<string:sub>/<string:bid>/', methods=['GET', 'POST'])
def records(sub, bid):
    if ("user" in session):  
        defaultData["pageCss"] = ["admin/records/records.css"]
        defaultData["menuItems"] = ""
        defaultData["adminItems"] = ["home", "signout"]
        defaultData["adminItemslinks"] = ["/Admin", "/signout"]  
        records = {
            "recordsdata": ["js/records.js"]
        }
        row = ""
        da = ""
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT bSubjects FROM `"+session['user']+"_batchs` WHERE id = "+bid+";")
            d = cur.fetchall()
            da = json.loads(d[0][0])
            mysql.connection.commit()
            cur.close()
            
            if(sub=="all"):
            
                cursor = mysql.connection.cursor()
                cursor.execute("select * from `"+session['user']+"_records` where bid = "+bid+";")
                
                row = cursor.fetchall()
                mysql.connection.commit()
                cursor.close()
            elif(sub=="tdayr"):
                today = date.today()
                print(today)
                cursor = mysql.connection.cursor()
                cursor.execute("select * from `"+session['user']+"_records` where bid = "+bid+" and edate = '"+str(today)+"';")
                row = cursor.fetchall()
                mysql.connection.commit()
                cursor.close()
                
            else:
                cursor = mysql.connection.cursor()
                today = date.today()
                cursor.execute("select * from `"+session['user']+"_records` where bid = "+bid+" and subject = '"+sub+"' and edate = '"+str(today)+"';")
                row = cursor.fetchall()
                mysql.connection.commit()
                cursor.close()
            
        except Exception as e:
            redirect("/Admin/creare-new-batch")
        return render_template("records.html", data=defaultData, records=records, row=row, d = da, id=bid)


@app.route('/Admin/scanner/<string:bid>/<string:sid>/<string:semail>', methods=['GET'])
def scanner(bid, semail, sid):
    if ("user" in session and session["user"] == semail):
        defaultData["pageCss"] = ["admin/scanner/scanner.css"]
        defaultData["menuItems"] = ""
        defaultData["adminItems"] = ["home", "signout"]
        defaultData["adminItemslinks"] = ["/Admin", "/signout"]  
        scanner = {
            "scannerdata": ["js/scanner.js"]
        }
        cur = mysql.connection.cursor()
        cur.execute("SELECT bsubjects FROM `"+session['user']+"_batchs` WHERE id= "+sid+";")
        d = cur.fetchall()
        da = json.loads(d[0][0])
        print(da)
        mysql.connection.commit()
        cur.close()
        
        return render_template("scanner.html", data=defaultData, scanner=scanner, d=da, semail=semail, sid=bid, bid=sid)
    else:
        return redirect("/")
        
        
@app.route('/Admin/addattendance/<string:sid>/<string:bid>/<string:umail>/<string:sub>', methods=['GET'])
def addattendance(sid,umail,sub, bid):
    if ("user" in session and session["user"] == umail):
        try:
            curtime = mysql.connection.cursor()
            curtime.execute("SELECT bsTime, beTime FROM `"+session["user"]+"_batchs` WHERE id = "+bid+";")
            recf = curtime.fetchall()
            print(recf)
            mysql.connection.commit()
            curtime.close()
            
            now = datetime.now()
            print(now)
            
            # stime = str(recf[0][0]) 
            # print(stime[0:2])
            # etime = str(recf[0][1]) 
            # print(etime[0:1])
            
            # dstime = now.replace(hour=int(stime[0:2]), minute=int(stime[3:6]), second=0, microsecond=0)
            # detime = now.replace(hour=int(etime[0:2]), minute=int(etime[3:6]), second=0, microsecond=0)
            # print(dstime)
            # print(detime)
            
            if(True):
                cur = mysql.connection.cursor()
                cur.execute("SELECT bid, name FROM `"+session['user']+"_students` WHERE sid= "+sid+" and bid = "+bid+";")
                d = cur.fetchall()
                mysql.connection.commit()
                cur.close()
                if(len(d)!=0):
                    checkcur = mysql.connection.cursor()
                    today = date.today()
                    print(today)
                    checkcur.execute("SELECT sid from `"+session["user"]+"_records` WHERE bid = "+bid+" AND sid = "+sid+" and subject = '"+sub+"' and edate = '"+str(today)+"';")
                    info = checkcur.fetchall()
                    print(info)
                    mysql.connection.commit()
                    checkcur.close()
                    cursor = mysql.connection.cursor()
                    
                    if(len(info) == 0):
                        cursor.execute("INSERT INTO `"+session["user"]+"_records` (`bid`, `sid`, `sname`, `etime`, `subject`, `edate`) VALUES ("+bid+", "+sid+", '"+d[0][1]+"', current_timestamp(), '"+sub+"', '"+str(today)+"');")
                        mysql.connection.commit()
                        cursor.close()
                        session["almsg"] = "Attendance Added Successfully...."
                        session["alcode"] = "alert alert-success"
                    else:
                        session["almsg"] = "your attendance for this subject is already exist...."
                        session["alcode"] = "alert alert-danger"
                else:
                    session["almsg"] = "Attendance Not Added..."
                    session["alcode"] = "alert alert-danger"
            else:
                session["almsg"] = "college is closed Attendance Not Added..."
                session["alcode"] = "alert alert-danger"
                
        except Exception as e:
            cur = mysql.connection.cursor()
            cur.execute("SELECT bid, name FROM `"+session['user']+"_students` WHERE sid= "+sid+";")
            d = cur.fetchall()
            # da = json.loads(d[0][0])
            print(d)
            mysql.connection.commit()
            cur.close()
            if(d!=0):
                cursor = mysql.connection.cursor()
                today = date.today()
                cursor.execute("CREATE TABLE `"+session['user']+"_records` (`id` INT AUTO_INCREMENT , `bid` INT NOT NULL , `sid` INT NOT NULL , `sname` TEXT NOT NULL , `etime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , `subject` TEXT NOT NULL , `edate` TEXT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;")
                cursor.execute("INSERT INTO `"+session["user"]+"_records` (`id`, `bid`, `sid`, `sname`, `etime`, `subject`, `edate`) VALUES ('1', "+bid+", "+sid+", '"+d[0][1]+"', current_timestamp(), '"+sub+"', '"+str(today)+"');")
                # d = cursor.fetchall()
                # da = json.loads(d[0][0])
                # print(len(d))
                mysql.connection.commit()
                cursor.close()
        return redirect("/")
    else:
        return redirect("/")

# INSERT INTO `records` (`id`, `bid`, `sid`, `sname`, `etime`, `subject`) VALUES ('1', '1', '1', 'niraj', current_timestamp(), 'dbms');


if __name__ == "__main__":
    app.run(debug=True)
