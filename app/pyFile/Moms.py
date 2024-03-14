import os
import sys
import math
import json
import datetime
import requests
import numpy as np
import pandas as pd
import mysql.connector
from bs4 import BeautifulSoup
from app.module import dbModule
from app.module import getReqInfo
from dateutil.relativedelta import relativedelta


def select_moms_index():
    db_class = dbModule.Database()
    sql = "SELECT 'NORMAL' TYPE,cls_date ,SUM(total) total_sum,SUM(inv) inv_sum,SUM(no_inv) no_inv_sum,SUM(emergen) emergen_sum,sum(cello) cello_sum,MAX(ins_date) ins_date, cast(IFNULL(FLOOR((SUM(inv)/SUM(total))*100),0) AS CHAR(20)) inv_per, CAST(IFNULL(CEIL((SUM(no_inv)/SUM(total))*100),0) AS CHAR(20)) no_inv_per FROM moms_outbound_data  WHERE cls_date = DATE_FORMAT(NOW(),'%Y%m%d') AND CUT_OFF_NO NOT LIKE '%_BT%' UNION ALL SELECT 'BUTIQUE' TYPE, ifnull(cls_date,DATE_FORMAT(NOW(),'%Y%m%d')) cls_date,ifnull(SUM(total),'0') total_sum,ifnull(SUM(inv),'0')  inv_sum,ifnull(SUM(no_inv),'0')   no_inv_sum,ifnull(SUM(emergen),'0')   emergen_sum,ifnull(sum(cello),'0')   cello_sum,ifnull(MAX(ins_date),DATE_FORMAT(NOW(),'%Y-%m-%d %T'))  ins_date , IFNULL(FLOOR((SUM(inv)/SUM(total))*100),0) inv_per, IFNULL(CEIL((SUM(no_inv)/SUM(total))*100),0) no_inv_per  FROM moms_outbound_data  WHERE cls_date = DATE_FORMAT(NOW(),'%Y%m%d') AND CUT_OFF_NO LIKE '%_BT%'"
    reVal = db_class.executeAll(sql)
    return reVal

def select_moms_Excel():
    db_class = dbModule.Database()
    sql = "SELECT C.* FROM (SELECT A.CUT_OFF_NO,A.CLS_DATE,A.CUT_SEQ,IFNULL(B.TOTAL,'-') TOTAL,IFNULL(B.INV,'-') INV,IFNULL(B.NO_INV,'-') NO_INV,IFNULL(B.CELLO,'-') CELLO,IFNULL(A.BZ_YN,'N') BZ_YN,IFNULL(B.MAKE_YN,'N') MAKE_YN ,IFNULL(B.EMER,'-') EMER,IFNULL(A.DOC_QTY,'-') DOC_QTY FROM moms_outbound_data AS A LEFT OUTER JOIN moms_excel_log AS B ON A.CUT_OFF_NO = B.CUT_OFF_NO AND A.CLS_DATE = B.CLS_DATE AND A.CUT_SEQ = B.CUT_SEQ )C WHERE C.CLS_DATE = DATE_FORMAT(NOW(),'%Y%m%d') ORDER BY C.CUT_SEQ,C.CUT_OFF_NO"
    print(sql)
    reVal = db_class.executeAll(sql)
    return reVal
   
def update_count_moms():
    user_id = 'heechan.lee@musinsa.com'
        #비제스트 컷오프명 가져오기
    req_url = 'https://bizest.musinsa.com/ho/order/ord36'
    r = requests.post(req_url+ str('?API_KEY=d1869a20cd1a6f12c42d41f714df3325&API_USER_ID=mss_632'))
    soup = BeautifulSoup(r.text,'lxml')
    select = soup.find("select",attrs={ "name":"S_DLV_SERIES_NO"})
    cutoffList = select.findAll('option')

    header = getReqInfo.getSessionInfo().getMomsinfo()
    now = datetime.datetime.now()
    nowDate = datetime.date(now.year, now.month, now.day)
    cls_date = nowDate.isoformat().replace('-','')
    url='https://moms.musinsa.com/api/grid/search/'   
    data = {'params':'{\"MENU_CD\":\"GI02_HEAD\",\"USR_ID\":\"heechan.lee@musinsa.com\",\"params\":{\"SPR_NM\":\"MUSINSA\",\"CLS_DATE\":[\"'+str(nowDate).replace("-","")+'\",\"'+str(nowDate).replace("-","")+'\"],\"CUT_OFF_NO\":\"\"},\"type\":\"click\",\"page\":1}'}
    jsonData= requests.post(url,headers=header,json=data).json()
    df = pd.DataFrame(jsonData['rtnData'])
    df = df[['SPR_NM','CLS_DATE','CUT_OFF_NO','CUT_SEQ']]
    df['BZ_YN'] = 'N'
    df['TOTAL']=0
    df['INV']=0
    df['NO_INV']=0
    df['EMERGEN']=0
    df['CELLO']=0
    dfa = df.copy()
        #비제스트에서 컷오프한 차수 표시
    for c in range(len(dfa)):
       cutoff_nm = str(dfa['CUT_OFF_NO'][c])
       for l in cutoffList:
        if str(l.text) == cutoff_nm:
            dfa = dfa.astype('str')
            dfa['BZ_YN'][c]='Y'

        #MOMS 차수별 카운트        
    calData = dfa.copy()
    calData = calData.astype('str')
    for d in range(len(calData)):
        data1 = {'params':'{\"params\":{\"TAB_IDX\":1,\"CLS_DATE\":\"'+str(calData['CLS_DATE'][d])+'\",\"CUT_SEQ\":'+str(calData['CUT_SEQ'][d])+',\"CUT_OFF_NO\":\"'+str(calData['CUT_OFF_NO'][d])+'\",\"SPR_NM\":\"MUSINSA\"},\"MENU_CD\":\"GI02_ITEM\",\"USR_ID\":\"'+user_id+'\"}'}
        jsonData1= requests.post(url,headers=header,json=data1).json()
        if jsonData1['rtnChk']!=False:
            calData['TOTAL'][d] = len(jsonData1['rtnData'])
            calData = calData.astype('str')
        
        # 할당
        data2 = {"params":'{\"params\":{\"TAB_IDX\":2,\"CLS_DATE\":\"'+str(calData['CLS_DATE'][d])+'\",\"CUT_SEQ\":'+str(calData['CUT_SEQ'][d])+',\"CUT_OFF_NO\":\"'+str(calData['CUT_OFF_NO'][d])+'\",\"SPR_NM\":\"MUSINSA\"},\"MENU_CD\":\"GI02_ITEM\",\"USR_ID\":\"'+user_id+'\"}'}
        jsonData2= requests.post(url,headers=header,json=data2).json()
        if jsonData2['rtnChk']!=False:
            calData['INV'][d] = len(jsonData2['rtnData'])
            calData = calData.astype('str')

        # 미할당
        data3 = {'params':'{\"params\":{\"TAB_IDX\":3,\"CLS_DATE\":\"'+str(calData['CLS_DATE'][d])+'\",\"CUT_SEQ\":'+str(calData['CUT_SEQ'][d])+',\"CUT_OFF_NO\":\"'+str(calData['CUT_OFF_NO'][d])+'\",\"SPR_NM\":\"MUSINSA\"},\"MENU_CD\":\"GI02_ITEM\",\"USR_ID\":\"'+user_id+'\"}'}
        jsonData3= requests.post(url,headers=header,json=data3).json()
        if jsonData3['rtnChk']!=False:
            calData['NO_INV'][d] = len(jsonData3['rtnData'])
            calData = calData.astype('str')

        # 이상발생
        data4 = {'params':'{\"params\":{\"TAB_IDX\":4,\"CLS_DATE\":\"'+str(calData['CLS_DATE'][d])+'\",\"CUT_SEQ\":'+str(calData['CUT_SEQ'][d])+',\"CUT_OFF_NO\":\"'+str(calData['CUT_OFF_NO'][d])+'\",\"SPR_NM\":\"MUSINSA\"},\"MENU_CD\":\"GI02_ITEM\",\"USR_ID\":\"'+user_id+'\"}'}
        jsonData4 = requests.post(url,headers=header,json=data4).json()
        if jsonData4['rtnChk']!=False:
            calData['EMERGEN'][d] = len(jsonData4['rtnData'])
            calData = calData.astype('str')

        # 첼로
        data5 = {'params':'{\"params\":{\"TAB_IDX\":5,\"CLS_DATE\":\"'+str(calData['CLS_DATE'][d])+'\",\"CUT_SEQ\":'+str(calData['CUT_SEQ'][d])+',\"CUT_OFF_NO\":\"'+str(calData['CUT_OFF_NO'][d])+'\",\"SPR_NM\":\"MUSINSA\"},\"MENU_CD\":\"GI02_ITEM\",\"USR_ID\":\"'+user_id+'\"}'}
        jsonData5= requests.post(url,headers=header,json=data5).json()
        if jsonData5['rtnChk']!=False:
            calData['CELLO'][d] = len(jsonData5['rtnData'])
            calData = calData.astype('str')
    
    row = [tuple(x) for x in calData.to_records(index=False)]
    con = mysql.connector.connect(user='root',password='antlstk1@',port='3306',host='localhost',database='managerdb')
    cursor = con.cursor()
    cursor.execute("DELETE  FROM moms_outbound_data WHERE CLS_DATE='"+str(cls_date)+"'")
    con.commit()
    cursor.executemany("INSERT INTO moms_outbound_data(SPR_NM,CLS_DATE,CUT_OFF_NO,CUT_SEQ,BZ_YN,TOTAL,INV,NO_INV,EMERGEN,CELLO,INS_DATE) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'"+format(datetime.datetime.now().strftime('%Y-%m-%d %T'))+"')",row)
    con.commit()

    # cursor.execute("select req_total_cnt,proc_total_cnt,btq_total_cnt,ins_date FROM bizest_outbound_info where 1=1 ")
    # result = cursor.fetchone()
    # con.close()    
    # return result
    



    
    return calData
    

