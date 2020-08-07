from flask import Flask, jsonify, flash, redirect, render_template, request, session, abort
import os
import pymysql as MySQLdb
import json
from datetime import datetime
from waitress import serve

import datetime
import random
import time

app = Flask(__name__)

minute=0
hour=0
summationHour=0
summationDay=0
summationMinute=0
# cnow =datetime.datetime.now()
# cmonth=cnow.month()

@app.route('/sendDataToSQL')
def sendDataToSQL():
    print("here")
    prediction()
    print("here1")
    return 'Data Sent'
 
def prediction():
    #the prediction code
    print("yes")
    return "YEs it does" 

app.run(host='0.0.0.0', port= 5000)


@app.route('/sendDataToSQL')
def sendDataToSQL():
    now =datetime.datetime.now()    
    month=str(now.year) +'-'+str(now.month)
    day=month+'-'+str(now.day)
    hour=day+' '+str(now.hour)
    minute=str(hour+':'+str(now.minute)+':00')
    node_id = request.args.get('node_id')
    voltage = request.args.get('voltage')
    current = request.args.get('current')
    db = MySQLdb.connect("localhost", "root", "", "e_meter")
    cursor = db.cursor()
    cursor.execute("select meterId from node_meterid where node_id='%s'"%(node_id))
    data = cursor.fetchall()
    meter_id=data[0][0]
    cursor.execute("INSERT INTO minute_wise (meterId,date_time, voltage, current) VALUES(%d, '%s', '%s','%s')"% (meter_id, minute,voltage, current))
    minute+=1
    summationMinute+=current
    if(minute==60):
        cursor.execute("INSERT INTO hour_wise (meterId,date_time,current) VALUES(%d,'%s','%s')"%(meter_id,summationMinute,minute))
        hour+=1
        minute=0
        summationMinute=0
        summationHour+=summationMinute
        if(hour==24):
            cursor.execute("INSERT INTO day_wise (meterId,current,datetime) VALUES(%d,'%s','%s')"%(meter_id,summationHour,day))
            hour=0
            summationHour=0
            summationDay+=summationHour
            if(c_month!=now.month()):
                cursor.execute("INSERT INTO month_wise (meterId,month_date,units,rooms,max_limit,cost,pred_units,pred_cost)values(%d,'%s',%d,%d,%d,%d,%d,%d)"%(meterId,month+"-01",summationDay,0,0,0,0,0))
                c_month=now.month()
                summationDay=0
                prediction()
    return 'Data Sent'