import json
from flask.helpers import make_response
import requests
import datetime
import  pandas as pd
import numpy as np
import pyautogui
import io
import os
import math
import sys
import mysql.connector
from io import BytesIO, StringIO
from bs4 import BeautifulSoup
from flask import Blueprint, request, render_template, flash, redirect, url_for,send_file
from flask import current_app as app
from app.module import dbModule,getReqInfo
from app.pyFile import Bizest,Moms,Cello,Common
from werkzeug.wrappers import response
 
schedule= Blueprint('schedule', __name__, url_prefix='/')

 
@schedule.route('/scheduleIndex', methods=['POST','GET'])
def scheduleIndex():
      auth = Common.getMacAddr()
      if auth=="Y":
            reTurnVal = Common.getBtqSchedule() 
            reTurnVal1 = Common.getNorSchedule() 
            return render_template('/html/schedule.html',resultDatabtq=reTurnVal,resultData=reTurnVal1)
      else:
            return render_template('/html/no-auth.html',authVal = auth)


@schedule.route('/saveNor', methods=['POST','GET'])
def saveNor():
      if request.method=='POST':
            # value = request.form.get('table1')
            selected = request.form.getlist("test")
            selected1 = request.form.getlist("test1")
            
            db_class = dbModule.Database()
            sql = "update batch_manager set chk='0' where type='일반'"
            sql1 = "update batch_manager set chk='0' where type='명품'"
            db_class.execute(sql)
            db_class.execute(sql1)
            db_class.commit()

            for i in selected:
                  sql = "update batch_manager set chk='1' where type='일반' and hour='"+i+"'"
                  db_class.execute(sql)
                  db_class.commit()
            for i in selected1:
                  sql = "update batch_manager set chk='1' where type='명품' and hour='"+i+"'"
                  db_class.execute(sql)
                  db_class.commit()

      return redirect(url_for("schedule.scheduleIndex"))
      


@schedule.route('/deleteAll', methods=['POST','GET'])
def deleteAll():
      db_class = dbModule.Database()
      sql = "update batch_manager set chk='0' where type='일반'"
      sql1 = "update batch_manager set chk='0' where type='명품'"
      db_class.execute(sql)
      db_class.execute(sql1)
      db_class.commit()
      
      
      return redirect(url_for("schedule.scheduleIndex"))
      
