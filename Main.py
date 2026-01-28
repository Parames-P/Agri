from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import os
import base64
from PIL import Image
from datetime import datetime
from datetime import date
from datetime import datetime, timedelta
import datetime
import random
from random import seed
from random import randint
from werkzeug.utils import secure_filename
from flask import send_file
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import threading
import time
import shutil
import hashlib
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="agri_rental"
)


app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####

@app.route('/',methods=['POST','GET'])
def index():
    cnt=0
    act=""
    msg=""
    mycursor = mydb.cursor()
    
    if request.method == 'POST':
        page = request.form['page']
        if page=="login":
            username1 = request.form['uname']
            password1 = request.form['pass']
            
            mycursor.execute("SELECT count(*) FROM ar_user where uname=%s && pass=%s",(username1,password1))
            myresult = mycursor.fetchone()[0]
            print(myresult)
            if myresult>0:
                session['username'] = username1
                
                return redirect(url_for('userhome')) 
            else:
                msg="no"

        elif page=="reg":
            name = request.form['name']
            address = request.form['address']
            district = request.form['district']
            mobile = request.form['mobile']
            email = request.form['email']
            uname = request.form['uname']
            pass1 = request.form['pass']

            mycursor.execute("SELECT count(*) FROM ar_user where uname=%s || email=%s",(uname,email))
            cnt = mycursor.fetchone()[0]
            if cnt==0:
                mycursor.execute("SELECT max(id)+1 FROM ar_user")
                maxid = mycursor.fetchone()[0]
                if maxid is None:
                    maxid=1
                sql = "INSERT INTO ar_user(id,name,address,district,mobile,email,uname,pass) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (maxid,name,address,district,mobile,email,uname,pass1)
                mycursor.execute(sql, val)
                mydb.commit()
                msg="success"
            else:
                msg="fail"
            
        

    return render_template('index.html',msg=msg,act=act)

@app.route('/login_pro',methods=['POST','GET'])
def login_pro():
    cnt=0
    act=""
    msg=""

    
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM ar_provider where uname=%s && pass=%s && status=1",(username1,password1))
        myresult = mycursor.fetchone()[0]
        print(myresult)
        if myresult>0:
            session['username'] = username1
            
            return redirect(url_for('pro_home')) 
        else:
            msg="Invalid Username or Password! or not approved"
            
        

    return render_template('login_pro.html',msg=msg,act=act)

@app.route('/login_admin',methods=['POST','GET'])
def login_admin():
    cnt=0
    act=""
    msg=""
    if request.method == 'POST':
        
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM ar_admin where username=%s && password=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            return redirect(url_for('admin')) 
        else:
            msg="You are logged in fail!!!"
        

    return render_template('login_admin.html',msg=msg,act=act)


@app.route('/reg_pro', methods=['GET', 'POST'])
def reg_pro():
    msg=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    

    if request.method=='POST':
        name=request.form['name']
        address=request.form['address']
        district=request.form['district']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']

        

        mycursor.execute("SELECT count(*) FROM ar_provider where uname=%s",(uname,))
        myresult = mycursor.fetchone()[0]

        if myresult==0:
        
            mycursor.execute("SELECT max(id)+1 FROM ar_provider")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            now = date.today() #datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
            
            sql = "INSERT INTO ar_provider(id,name,address,district,mobile,email,uname,pass,create_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,name,address,district,mobile,email,uname,pass1,rdate)
            mycursor.execute(sql, val)
            mydb.commit()

            
            print(mycursor.rowcount, "Registered Success")
            msg="success"
            
            #if cursor.rowcount==1:
            #    return redirect(url_for('index',act='1'))
        else:
            
            msg='fail'
            
    
    return render_template('reg_pro.html', msg=msg)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    act=request.args.get("act")
    email=""
    mess=""
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT * FROM ar_provider")
    data = mycursor.fetchall()

    if act=="ok":
        pid=request.args.get("pid")
        mycursor.execute("update ar_provider set status=1 where id=%s",(pid,))
        mydb.commit()
        msg="success"
    
    
    return render_template('admin.html',msg=msg,data=data,act=act)


@app.route('/pro_home', methods=['GET', 'POST'])
def pro_home():
    msg=""
    act=""
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(uname, ))
    data = mycursor.fetchone()

    
    return render_template('pro_home.html',data=data,act=act)


@app.route('/pro_add', methods=['GET', 'POST'])
def pro_add():
    msg=""
    act=""
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(uname, ))
    data = mycursor.fetchone()

    if request.method=='POST':
        vehicle=request.form['vehicle']
        vno=request.form['vno']
        details=request.form['details']
        cost1=request.form['cost1']
        cost2=request.form['cost2']
        file= request.files['file']

        mycursor.execute("SELECT max(id)+1 FROM ar_vehicle")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")

        if file:
            fname1 = file.filename
            fname = secure_filename(fname1)
            photo="P"+str(maxid)+fname
            file.save(os.path.join("static/upload/", photo))
                
        sql = "INSERT INTO ar_vehicle(id,uname,vehicle,vno,details,cost1,cost2,photo,create_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,uname,vehicle,vno,details,cost1,cost2,photo,rdate)
        mycursor.execute(sql, val)
        mydb.commit()
        msg="success"
        

        
    return render_template('pro_add.html',msg=msg,data=data,act=act)

@app.route('/pro_vehicle', methods=['GET', 'POST'])
def pro_vehicle():
    msg=""
    act=""
    uname=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    print(uname)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(uname, ))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ar_vehicle where uname=%s",(uname, ))
    dd2 = mycursor.fetchall()

    for ds2 in dd2:
        dt=[]
        dt.append(ds2[0])
        dt.append(ds2[1])
        dt.append(ds2[2])
        dt.append(ds2[3])
        dt.append(ds2[4])
        dt.append(ds2[5])
        dt.append(ds2[6])
        dt.append(ds2[7])
        dt.append(ds2[8])
        dt.append(ds2[9])
        s1="2"
        ss=""
        mycursor.execute("SELECT count(*) FROM ar_booking where provider=%s && vid=%s && status=0",(uname, ds2[0]))
        cnt3 = mycursor.fetchone()[0]
        if cnt3>0:
            s1="1"
            ss=str(cnt3)

        print("ss="+ss)

        dt.append(ss)
        dt.append(s1)
        data2.append(dt)
        

    return render_template('pro_vehicle.html',msg=msg,data=data,act=act,data2=data2)

@app.route('/pro_request', methods=['GET', 'POST'])
def pro_request():
    msg=""
    vid=request.args.get("vid")
    act=request.args.get("act")
    uname=""
    st=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    print(uname)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(uname, ))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ar_vehicle where id=%s",(vid, ))
    vdata = mycursor.fetchone()

    mycursor.execute("SELECT count(*) FROM ar_booking where provider=%s && vid=%s && status<=1",(uname, vid))
    cnt3 = mycursor.fetchone()[0]

    if cnt3>0:
        st="1"
        mycursor.execute("SELECT * FROM ar_booking b, ar_user a where b.uname=a.uname && b.provider=%s && b.vid=%s && b.status<=1",(uname, vid))
        data2 = mycursor.fetchall()
        
       
    if act=="ok":
        bid=request.args.get("bid")
        provided_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        mycursor.execute("update ar_booking set status=1, provided_time=%s where id=%s", (provided_time,bid))
        mydb.commit()
        mycursor.execute("update ar_vehicle set status=1 where id=%s", (vid,))
        mydb.commit()
        msg="ok"
        
    return render_template('pro_request.html',msg=msg,data=data,act=act,data2=data2,vdata=vdata,st=st,vid=vid)



@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""
    act=""
    uname=""
    st=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    
    print('uname:',uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_user where uname=%s",(uname, ))
    data = mycursor.fetchone()

    if request.method=='POST':
        search=request.form['search']
        st="1"

        gs='%'+search+'%'

        uu=[]
        mycursor.execute("SELECT * FROM ar_provider where name like %s || address like %s || district like %s",(gs,gs,gs))
        dd2 = mycursor.fetchall()
        for ds2 in dd2:
            uu.append(ds2[6])

        print(uu,"###")
        if len(uu)>0:
            for u1 in uu:
                mycursor.execute("SELECT * FROM ar_vehicle where uname=%s && status=0",(u1,))
                dd3 = mycursor.fetchall()
                for ds3 in dd3:
                    data2.append(ds3)
                
                
        else:
            mycursor.execute("SELECT * FROM ar_vehicle where (uname like %s || vehicle like %s || vno like %s || details like %s) && status=0",(gs,gs,gs,gs))
            data2 = mycursor.fetchall()
        

    if st=="":
        mycursor.execute("SELECT * FROM ar_vehicle where status=0 order by rand() limit 0,10")
        data2 = mycursor.fetchall()
        print(data2,"...")
    return render_template('userhome.html',data=data,act=act,data2=data2)

@app.route('/book', methods=['GET', 'POST'])
def book():
    msg=""
    act=""
    uname=""
    st=""
    amt=0
    vid=request.args.get("vid")
    print(vid,".............")
    data2=[]
    if 'username' in session:
        uname = session['username']

    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_user where uname=%s",(uname, ))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ar_vehicle where id=%s",(vid,))
    dd = mycursor.fetchone()
    pro=dd[1]
    cost1=dd[5]
    cost2=dd[6]
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(pro,))
    pdata = mycursor.fetchone()
    provider=pdata[6]
        

    if request.method=='POST':
        duration=request.form['duration']
        time_type=request.form['time_type']
        req_date=request.form['req_date']

        mycursor.execute("SELECT max(id)+1 FROM ar_booking")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        tt=int(duration)
        if time_type=="1":
            amt=cost1*tt
        else:
            amt=cost2*tt
        
        sql = "INSERT INTO ar_booking(id,uname,provider,vid,duration,time_type,req_date,status,amount,pay_st) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,uname,provider,vid,duration,time_type,req_date,'0',amt,'0')
        mycursor.execute(sql, val)
        mydb.commit()
        msg="success"
        

    return render_template('book.html',msg=msg,data=data,act=act,pdata=pdata)



@app.route('/user_status', methods=['GET', 'POST'])
def user_status():
    msg=""
    act=""
    uname=""
    st=""
    data2=[]
    if 'username' in session:
        uname = session['username']
        
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_user where uname=%s",(uname, ))
    data = mycursor.fetchone()

    
    mycursor.execute("SELECT * FROM ar_vehicle v,ar_booking b where v.id=b.vid && b.uname=%s order by b.id desc",(uname,))
    data2 = mycursor.fetchall()
    
    return render_template('user_status.html',data=data,act=act,data2=data2)
'''
@app.route('/user_pay', methods=['GET', 'POST'])
def user_pay():
    msg=""
    act=""
    uname=""
    bid=request.args.get("bid")
    vid=request.args.get("vid")
    st=""
    data2=[]
    if 'username' in session:
        uname = session['username']
        
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_user where uname=%s",(uname, ))
    data = mycursor.fetchone()

    
    mycursor.execute("SELECT * FROM ar_vehicle v,ar_booking b where v.id=b.vid && b.uname=%s && b.id=%s",(uname,bid))
    data2 = mycursor.fetchone()

    if request.method=='POST':
        card=request.form['card']
        
        mycursor.execute("update ar_booking set status=2 where id=%s", (bid,))
        mydb.commit()
        mycursor.execute("update ar_vehicle set status=0 where id=%s", (vid,))
        mydb.commit()
        msg="ok"
        
    
    return render_template('user_pay.html',msg=msg,data=data,act=act,data2=data2)
'''
@app.route('/user_pay', methods=['GET', 'POST'])
def user_pay():
    msg = ""
    data=""
    uname = session.get('username')
    bid = request.args.get("bid")
    vid = request.args.get("vid")
    
    #if not uname:
        #return "Unauthorized Access"

    mycursor = mydb.cursor()

    # Fetch user details
    mycursor.execute("SELECT * FROM ar_user WHERE uname=%s", (uname,))
    user_data = mycursor.fetchone()

    
    # Fetch vehicle & booking details
    mycursor.execute("SELECT b.vid, b.duration, b.time_type, b.provided_time, b.amount, v.cost2 FROM ar_booking b JOIN ar_vehicle v ON b.vid = v.id WHERE b.uname=%s AND b.id=%s", (uname, bid))
    data = mycursor.fetchone()
    print(data,"data......")

    if not data:
        return "Booking not found."

    #vid, _, _, _, _, duration, time_type, provided_time, amount = booking_data
    vid, duration, time_type, provided_time, amount, normal_rate = data

    # Convert provided_time to datetime format
    from datetime import datetime
    if isinstance(provided_time, str):
        provided_time = datetime.strptime(provided_time, '%Y-%m-%d %H:%M:%S')
    #provided_time = datetime.strptime(provided_time, '%Y-%m-%d %H:%M:%S')

    # Calculate allowed return time
    if time_type == "1":  # Hours
        allowed_return_time = provided_time + timedelta(hours=int(duration))
        print(allowed_return_time,"allowed_return_time")
    else:  # Days
        allowed_return_time = provided_time + timedelta(days=int(duration))

    # Get current time
    current_time = datetime.now()
    fine_amount = 0
    
    # Fine calculation if exceeded
    if current_time > allowed_return_time:
        fine_rate = normal_rate*2  # Fine per extra hour
        print(fine_rate)
        extra_hours = (current_time - allowed_return_time).total_seconds() / 3600
        fine_amount = int(extra_hours) + fine_rate
    print(fine_amount,"##########")
    # Calculate total amount with fine
    total_amount = amount + fine_amount

    if request.method == 'POST':
        card = request.form['card']

        # Update booking status & total amount
        mycursor.execute("UPDATE ar_booking SET status=2, amount=%s WHERE id=%s", (total_amount, bid))
        mycursor.execute("UPDATE ar_vehicle SET status=0 WHERE id=%s", (vid,))
        mydb.commit()
        
        msg = f"Payment Successful! Total Amount: Rs. {total_amount} (including fine Rs. {fine_amount})"

    return render_template('user_pay.html', msg=msg, data=data, amount=amount, user_data=user_data, fine_amount=fine_amount, total_amount=total_amount)

@app.route('/view_pro', methods=['GET', 'POST'])
def view_pro():
    msg=""
    act=""
    uname=request.args.get("uname")
    data2=[]
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(uname, ))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ar_vehicle where uname=%s",(uname, ))
    dd2 = mycursor.fetchall()

    for ds2 in dd2:
        dt=[]
        dt.append(ds2[0])
        dt.append(ds2[1])
        dt.append(ds2[2])
        dt.append(ds2[3])
        dt.append(ds2[4])
        dt.append(ds2[5])
        dt.append(ds2[6])
        dt.append(ds2[7])
        dt.append(ds2[8])
        dt.append(ds2[9])
        s1="2"
        ss=""
        mycursor.execute("SELECT count(*) FROM ar_booking where provider=%s && vid=%s && status=0",(uname, ds2[0]))
        cnt3 = mycursor.fetchone()[0]
        if cnt3>0:
            s1="1"
            ss=str(cnt3)

        print("ss="+ss)

        dt.append(ss)
        dt.append(s1)
        data2.append(dt)
        

    return render_template('view_pro.html',msg=msg,data=data,act=act,data2=data2,uname=uname)

@app.route('/aboutus')
def aboutus():

    return render_template('aboutus.html')

@app.route('/pro_history', methods=['GET', 'POST'])
def pro_history():
    msg=""
    act=""
    uname=""
    st=""
    data2=[]
    if 'username' in session:
        uname = session['username']
        
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(uname, ))
    data = mycursor.fetchone()

    
    mycursor.execute("SELECT * FROM ar_vehicle v,ar_booking b where v.id=b.vid && b.provider=%s && b.status=2 order by b.id desc",(uname,))
    data2 = mycursor.fetchall()
    
    return render_template('pro_history.html',data=data,act=act,data2=data2)

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
