import os
import json
import datetime
import requests
import numpy as np
import pandas as pd
import mysql.connector
from bs4 import BeautifulSoup
from app.module import dbModule
from dateutil.relativedelta import relativedelta


def select_index():
    db_class = dbModule.Database()
    sql = "select IFNULL((req_nor_cnt+req_btq_cnt),0) total_req,IFNULL((proc_nor_cnt+proc_btq_cnt),0) total_proc,IFNULL(req_btq_cnt,0) req_btq_cnt,IFNULL(proc_btq_cnt,0)  proc_btq_cnt,IFNULL(req_nor_cnt,0)  req_nor_cnt,IFNULL(proc_nor_cnt,0)  proc_nor_cnt,IFNULL(Floor((req_nor_cnt/(req_nor_cnt+req_btq_cnt))*100),0) req_nor_per,IFNULL(Floor((proc_nor_cnt/(proc_nor_cnt+proc_btq_cnt)*100)),0) proc_nor_per,IFNULL(CEIL((req_btq_cnt/(req_nor_cnt+req_btq_cnt))*100),0) req_btn_per,IFNULL(CEIL((proc_btq_cnt/(proc_nor_cnt+proc_btq_cnt))*100),0) proc_btn_per,ins_date FROM bizest_outbound_info where 1=1"
    reVal = db_class.executeOne(sql)
    return reVal
    
def select_BZ_data():
    db_class = dbModule.Database()
    sql = "SELECT CUT_OFF_NO,CUT_OFF_CNT FROM bizest_outbound_data WHERE CLS_DATE = DATE_FORMAT(NOW(),'%Y%m%d') ORDER BY CUT_OFF_NO"
    reVal = db_class.executeAll(sql)
    return reVal

def update_count_bizest():
    os.putenv('NLS_LANG', '.UTF8')
    now = datetime.datetime.now()
    beforeDate = datetime.date(now.year, now.month,now.day) - relativedelta(months=3)
    nowDate = datetime.date(now.year, now.month,now.day)

    cuttOffreq_url1 = 'https://bizest.musinsa.com/ho/api/order/ord35/search'
    cuttOffreq_url2 = 'https://bizest.musinsa.com/ho/api/order/ord36/search'
    
    cuttOffparams = {
                'USR_SEARCH_ITEM_CNT': '20',
                'S_DATE_CHK': 'ord_date',
                'DATE_TYPE': '0',
                'S_SDATE': beforeDate.isoformat(),
                'S_EDATE': nowDate.isoformat(),
                'S_ORD_STATE': '10',
                'S_COM_TYPE': '1',
                'S_EX_DLV_DUE_TYPE': 'Y',
                'CHK_P_CLM_STATE': 'Y',
                'ORD_FIELD': 'a.ord_no,a.ord_opt_no',
                'PAGE':1
    }
    r = requests.post(cuttOffreq_url1+str('?API_KEY=d1869a20cd1a6f12c42d41f714df3325&API_USER_ID=mss_632'), cuttOffparams)
    req_Normal_out_CNT = int(json.loads(r.text)['total'])
        

    cuttOffparams2 = {
        'USR_SEARCH_ITEM_CNT': '20',
        'DATE_TYPE': '0',
        'S_SDATE': beforeDate.isoformat(),
        'S_EDATE': nowDate.isoformat(),
        'S_ORD_STATE': '10',
        'S_COM_TYPE': '1',
        'S_DLV_DUE_TYPE': 'D',
        'CHK_P_CLM_STATE': 'Y',
        'ORD_FIELD': 'a.ord_no,a.ord_opt_no',
        'PAGE': '1'
    }

    r = requests.post(cuttOffreq_url1+str('?API_KEY=d1869a20cd1a6f12c42d41f714df3325&API_USER_ID=mss_632'), cuttOffparams2)
    req_Normal_out_CNT = req_Normal_out_CNT+int(json.loads(r.text)['total'])

    cuttOffparams = {
                'USR_SEARCH_ITEM_CNT': '20',
                'S_DATE_CHK': 'ord_date',
                'DATE_TYPE': '0',
                'S_SDATE': beforeDate.isoformat(),
                'S_EDATE': nowDate.isoformat(),
                'S_COM_NM':'musinsaboutique',
                'S_COM_ID':'musinsaboutique',
                'S_ORD_STATE': '10',
                'S_COM_TYPE': '1',
                'S_EX_DLV_DUE_TYPE': 'Y',
                'CHK_P_CLM_STATE': 'Y',
                'ORD_FIELD': 'a.ord_no,a.ord_opt_no',
                'PAGE':1
    }
    r = requests.post(cuttOffreq_url1+str('?API_KEY=d1869a20cd1a6f12c42d41f714df3325&API_USER_ID=mss_632'), cuttOffparams)
    req_BtQ_out_CNT = int(json.loads(r.text)['total'])

    cuttOffparams = {
                'USR_SEARCH_ITEM_CNT': '9',
                'S_DATE_KIND': 'ord_date',
                'DATE_TYPE_ORD': '0',
                'DATE_TYPE_DLV': '0',
                'S_SDATE': beforeDate.isoformat(),
                'S_EDATE': nowDate.isoformat(),
                'S_COM_NM':'musinsaboutique',
                'S_COM_ID':'musinsaboutique',
                'S_ORD_STATE': '20',
                'S_COM_TYPE': '1',
                'S_EX_DLV_DUE_TYPE': 'Y',        
                'PAGE': '1'                
    }
    r = requests.post(cuttOffreq_url2+str('?API_KEY=d1869a20cd1a6f12c42d41f714df3325&API_USER_ID=mss_632'), cuttOffparams)
    proc_BtQ_out_CNT = int(json.loads(r.text)['total'])
    
    cuttOffparams = {
        'USR_SEARCH_ITEM_CNT': '9',
        'S_DATE_KIND': 'ord_date',
        'DATE_TYPE_ORD': '0',
        'DATE_TYPE_DLV': '0',
        'S_SDATE': beforeDate.isoformat(),
        'S_EDATE': nowDate.isoformat(),
        'S_ORD_STATE': '20',
        'S_COM_TYPE': '1',
        'S_EX_DLV_DUE_TYPE': 'Y',        
        'PAGE': '1'
    }
    r = requests.post(cuttOffreq_url2+str('?API_KEY=d1869a20cd1a6f12c42d41f714df3325&API_USER_ID=mss_632'), cuttOffparams)
    proc_Normal_out_CNT = int(json.loads(r.text)['total'])
    
    con = mysql.connector.connect(user='root',password='antlstk1@',port='3306',host='localhost',database='managerdb')
    cursor = con.cursor()
    cursor.execute("DELETE  FROM bizest_outbound_info")
    con.commit()
    cursor.execute("INSERT INTO bizest_outbound_info(req_nor_cnt,proc_nor_cnt,req_btq_cnt,proc_btq_cnt,ins_date) values ('"+str(req_Normal_out_CNT-req_BtQ_out_CNT)+"','"+str(proc_Normal_out_CNT-proc_BtQ_out_CNT)+"','"+str(req_BtQ_out_CNT)+"','"+str(proc_BtQ_out_CNT)+"','"+format(datetime.datetime.now().strftime('%Y-%m-%d %T'))+"')")
    con.commit()
    

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

