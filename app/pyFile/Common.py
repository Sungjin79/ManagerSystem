import os
import json
import socket
import getmac
import datetime
import requests
import numpy as np
import pandas as pd
import mysql.connector
from flask import request
from bs4 import BeautifulSoup
from app.module import dbModule
from dateutil.relativedelta import relativedelta


def getMyIp():
    return request.environ.get('HTTP_X_REAL_IP',request.remote_addr)
    # return socket.gethostbyname(socket.getfqdn()) #host IP get

def getMacAddr():
    
    macaddr = getmac.get_mac_address()
    ip=getMyIp()
        
    db_class = dbModule.Database()
    sql = "SELECT user from mmg_auth where ip='"+ip+"'"
    result = db_class.executeOne(sql)
    if result == None:
        sql = "insert into mmg_auth(ip,com_name) value ( '"+ip+"','"+socket.getfqdn()+"')"
        db_class.execute(sql)
        db_class.commit()
        result = 'N'
    else:
        result = result[0]
    
    return  result

def getSlackToken():
    reval = "xoxb-511986659687-2558335142900-25r5LhMFuMDcNwOAsKdtFIZZ"
    return reval

def createDirectory(path): 
    try: 
        if not os.path.exists(path): 
            os.makedirs(path) 
    except :
        OSError: print("Error: Failed to create the directory.")

def slack_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)

def getMomsCutoffinfo(cut_off_nm):
    db_class = dbModule.Database()
    sql = "SELECT cls_date,cut_seq from moms_outbound_data where cut_off_no='"+cut_off_nm+"'"
    result = db_class.executeOne(sql)
    return result

def getBtqSchedule():
    db_class = dbModule.Database()
    sql = "SELECT type,hour,chk from batch_manager where type='명품'"
    result = db_class.executeAll(sql)
    return result

def getNorSchedule():
    db_class = dbModule.Database()
    sql = "SELECT type,hour,chk from batch_manager where type='일반'"
    result = db_class.executeAll(sql)
    return result
    
def get_bizest_data():
    os.putenv('NLS_LANG', '.UTF8')    
    now = datetime.datetime.now()
    nowDate = datetime.date(now.year, now.month, now.day)
    cls_date = nowDate.isoformat().replace('-','')
    beforeDate = datetime.date(now.year, now.month,now.day) - relativedelta(months=3)
    nowDate = datetime.date(now.year, now.month,now.day)

    cuttOffreq_url2 = 'https://bizest.musinsa.com/ho/api/order/ord36/search'

    con = mysql.connector.connect(user='root',password='antlstk1@',port='3306',host='localhost',database='managerdb')
    cursor = con.cursor()
    cursor.execute("DELETE  FROM bizest_outbound_data WHERE CLS_DATE='"+str(cls_date)+"'")
    con.commit()
    
    cursor.execute("SELECT CUT_OFF_NO,CLS_DATE,CUT_SEQ FROM moms_outbound_data WHERE bz_yn='Y' AND cls_date=DATE_FORMAT(NOW(),'%Y%m%d')")    
    reval = cursor.fetchall()

    for row in reval:
        req_url = 'https://bizest.musinsa.com/ho/order/ord36'
        r = requests.post(req_url+str('?API_KEY=d1869a20cd1a6f12c42d41f714df3325&API_USER_ID=mss_632') )
        soup = BeautifulSoup(r.text,'lxml')
        select = soup.find("select", attrs={"name": "S_DLV_SERIES_NO"})
        list = select.findAll('option')
        BzCode=''
        for l in list:
            if (l.text == row[0]):
                BzCode=l['value']
                break
        
        cuttOffparams = {
        'USR_SEARCH_ITEM_CNT': '9',
        'S_DATE_KIND': 'ord_date',
        'DATE_TYPE_ORD': '0',
        'DATE_TYPE_DLV': '0',
        'S_SDATE': beforeDate.isoformat(),
        'S_EDATE': nowDate.isoformat(),
        'S_ORD_STATE': '20',
        'S_COM_TYPE': '1',
        # 'S_EX_DLV_DUE_TYPE': 'Y',
        'S_DLV_SERIES_NO' :  BzCode,       
        'PAGE': '1'
        }   
        r = requests.post(cuttOffreq_url2+str('?API_KEY=d1869a20cd1a6f12c42d41f714df3325&API_USER_ID=mss_632'), cuttOffparams)
        series_out_CNT = int(json.loads(r.text)['total'])
        cursor.executemany("INSERT INTO bizest_outbound_data(CUT_OFF_NO,CLS_DATE,CUT_SEQ,CUT_OFF_CNT,INS_DATE) values (%s,%s,%s,'"+str(series_out_CNT)+"','"+format(datetime.datetime.now().strftime('%Y-%m-%d %T'))+"')",[row])
        con.commit()
        
    con.close()




        
        


    
