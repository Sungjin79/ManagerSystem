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
from app.module import dbModule,getReqInfo
from app.pyFile import Bizest,Moms,Cello,Common
from dateutil.relativedelta import relativedelta
from UliPlot.XLSX import auto_adjust_xlsx_column_width as autow


def select_cello_index():
    db_class = dbModule.Database()
    sql = "select IFNULL(total_pak_cnt,0) total_pak_cnt,IFNULL(total_nopak_cnt,0) total_nopak_cnt,IFNULL(nor_pak_cnt,0) nor_pak_cnt,IFNULL(nor_nopak_cnt,0) nor_nopak_cnt,IFNULL(btq_pak_cnt,0) btq_pak_cnt,IFNULL(btq_nopak_cnt,0) btq_nopak_cnt,IFNULL(btq_cj_pak_cnt,0) btq_cj_pak_cnt,IFNULL(btq_cj_nopak_cnt,0) btq_cj_nopak_cnt,ins_date, IFNULL((btq_pak_cnt+btq_cj_pak_cnt),0) btq_paked_cnt,IFNULL((btq_nopak_cnt+btq_cj_nopak_cnt),0) btq_nopacked_cnt ,IFNULL(FLOOR((nor_pak_cnt/(nor_pak_cnt+nor_nopak_cnt))*100),0) nor_pak_per,IFNULL(CEIL((nor_nopak_cnt/(nor_pak_cnt+nor_nopak_cnt))*100),0) nor_nopak_per,ifnull(FLOOR(((btq_pak_cnt+btq_cj_pak_cnt)/(btq_pak_cnt+btq_cj_pak_cnt+btq_nopak_cnt+btq_cj_nopak_cnt))*100),0) btq_pak_per,ifnull(CEIL(((btq_nopak_cnt+btq_cj_nopak_cnt)/(btq_pak_cnt+btq_cj_pak_cnt+btq_nopak_cnt+btq_cj_nopak_cnt))*100),0) btq_nopak_per  from cello_outbound_info where 1=1"
    reVal = db_class.executeOne(sql)
    return reVal

def select_moms_cello_count():
    db_class = dbModule.Database()
    sql = "SELECT (SELECT COUNT(*) FROM moms_request_data) CNT1,(SELECT COUNT(*) FROM cello_request_data) CNT2,(SELECT COUNT(*) FROM moms_request_data WHERE cut_off_no LIKE '%_BT%') CNT3,(SELECT DATE_FORMAT(max(ins_date), '%Y-%m-%d')  ins_date FROM cello_request_data) cello_ins_date,(SELECT MAX(FILE_NAME) UPLOAD_FILENAME FROM moms_request_data) UPLOAD_FILENAME,(SELECT MAX(FILE_NAME) UPLOAD_FILENAME FROM moms_request_data WHERE cut_off_no LIKE '%_BT%') UPLOAD_FILENAME2"
    reVal = db_class.executeOne(sql)
    return reVal

def select_cello_data():
    db_class = dbModule.Database()
    sql = "select status,stat_cnt,pack_yn FROM cello_outbound_data order by inx"
    reVal = db_class.executeAll(sql)    
    return reVal

def update_count_cello():    
    header = getReqInfo.getSessionInfo().getCelloinfo()
    now = datetime.datetime.now()
    to_date = datetime.date(now.year, now.month, now.day)
    req_url = 'https://cello.samsungscl.com/cello/wms/integration/json/WMS_OBO_97_001'
    timeCello = datetime.date(now.year, now.month, now.day)

    timeCello1 = timeCello + datetime.timedelta(days=-5)
    timeCello2 = timeCello1 + datetime.timedelta(days=1)
    param1 = "T15:00:00.000Z"
    param2 = "T14:59:59.000Z"

    total_paking = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],"tr_read":{"readtype":2,"readindex":0,"readcount":1},"querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,"toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"","refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"","telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9","packYn":"Y","strrId":"","cartnNo":"","packScd":"","giTcd":"","trnsTcd":"","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"","dlvrySts":"","shiptoId":"MUSINSA","soNo":"","poNo":"","addrReqYn":"","waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"","salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"","prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},"protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}
    r = requests.post(req_url, headers=header,json=total_paking)
    total_packing_Count = [json.loads(r.text)['rowcount']][0]

    total_no_paking = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],"tr_read":{"readtype":2,"readindex":0,"readcount":1},"querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,"toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"","refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"","telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9","packYn":"N","strrId":"","cartnNo":"","packScd":"","giTcd":"","trnsTcd":"","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"","dlvrySts":"","shiptoId":"MUSINSA","soNo":"","poNo":"","addrReqYn":"","waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"","salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"","prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},"protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}
    r = requests.post(req_url, headers=header,json=total_no_paking)
    total_nopacking_Count = [json.loads(r.text)['rowcount']][0]

    nor_paking = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],"tr_read":{"readtype":2,"readindex":0,"readcount":1},"querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,"toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"","refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"","telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9","packYn":"Y","strrId":"","cartnNo":"","packScd":"","giTcd":"","trnsTcd":"00","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"","dlvrySts":"","shiptoId":"MUSINSA","soNo":"","poNo":"","addrReqYn":"","waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"","salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"","prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},"protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}
    r = requests.post(req_url, headers=header,json=nor_paking)
    packing_CJ_Count = [json.loads(r.text)['rowcount']][0]

    nor_no_paking = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],"tr_read":{"readtype":2,"readindex":0,"readcount":1},"querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,"toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"","refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"","telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9","packYn":"N","strrId":"","cartnNo":"","packScd":"","giTcd":"","trnsTcd":"00","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"","dlvrySts":"","shiptoId":"MUSINSA","soNo":"","poNo":"","addrReqYn":"","waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"","salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"","prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},"protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}
    r = requests.post(req_url, headers=header,json=nor_no_paking)
    nopacking_CJ_Count = [json.loads(r.text)['rowcount']][0]

    btq_nor_paking = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],"tr_read":{"readtype":2,"readindex":0,"readcount":1},"querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,"toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"","refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"","telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9","packYn":"Y","strrId":"","cartnNo":"","packScd":"","giTcd":"","trnsTcd":"37","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"","dlvrySts":"","shiptoId":"MUSINSA","soNo":"","poNo":"","addrReqYn":"","waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"","salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"","prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},"protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}
    r = requests.post(req_url, headers=header,json=btq_nor_paking)
    btq_packing_Count = [json.loads(r.text)['rowcount']][0]

    btq_nor_no_paking = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],"tr_read":{"readtype":2,"readindex":0,"readcount":1},"querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,"toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"","refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"","telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9","packYn":"N","strrId":"","cartnNo":"","packScd":"","giTcd":"","trnsTcd":"37","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"","dlvrySts":"","shiptoId":"MUSINSA","soNo":"","poNo":"","addrReqYn":"","waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"","salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"","prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},"protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}
    r = requests.post(req_url, headers=header,json=btq_nor_no_paking)
    btq_nopacking_Count = [json.loads(r.text)['rowcount']][0]

    btq_cj_paking = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],"tr_read":{"readtype":2,"readindex":0,"readcount":1},"querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,"toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"","refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"","telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9","packYn":"Y","strrId":"","cartnNo":"","packScd":"","giTcd":"","trnsTcd":"38","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"","dlvrySts":"","shiptoId":"MUSINSA","soNo":"","poNo":"","addrReqYn":"","waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"","salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"","prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},"protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}
    r = requests.post(req_url, headers=header,json=btq_cj_paking)
    btq_CJ_packing_Count = [json.loads(r.text)['rowcount']][0]

    btq_cj_no_paking = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],"tr_read":{"readtype":2,"readindex":0,"readcount":1},"querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,"toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"","refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"","telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9","packYn":"N","strrId":"","cartnNo":"","packScd":"","giTcd":"","trnsTcd":"38","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"","dlvrySts":"","shiptoId":"MUSINSA","soNo":"","poNo":"","addrReqYn":"","waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"","salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"","prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},"protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}
    r = requests.post(req_url, headers=header,json=btq_cj_no_paking)
    btq_CJ_nopacking_Count = [json.loads(r.text)['rowcount']][0]
    
    con = mysql.connector.connect(user='root',password='antlstk1@',port='3306',host='localhost',database='managerdb')
    cursor = con.cursor()
    cursor.execute("DELETE  FROM cello_outbound_info")
    cursor.execute("DELETE  FROM cello_outbound_data")
    con.commit()
    cursor.execute("INSERT INTO cello_outbound_info(total_pak_cnt,total_nopak_cnt,nor_pak_cnt,nor_nopak_cnt,btq_pak_cnt,btq_nopak_cnt,btq_cj_pak_cnt,btq_cj_nopak_cnt,ins_date) values ('"+str(total_packing_Count)+"','"+str(total_nopacking_Count)+"','"+str(packing_CJ_Count)+"','"+str(nopacking_CJ_Count)+"','"+str(btq_packing_Count)+"','"+str(btq_nopacking_Count)+"','"+str(btq_CJ_packing_Count)+"','"+str(btq_CJ_nopacking_Count)+"','"+format(datetime.datetime.now().strftime('%Y-%m-%d %T'))+"')")
    cursor.execute("INSERT INTO cello_outbound_data(pack_yn,inx,status,stat_cnt,ins_date) values ('Y',1,'전체 패킹완료','"+str(total_packing_Count)+"','"+format(datetime.datetime.now().strftime('%Y-%m-%d %T'))+"')")
    cursor.execute("INSERT INTO cello_outbound_data(pack_yn,inx,status,stat_cnt,ins_date) values ('N',2,'전체 패킹 미완료','"+str(total_nopacking_Count)+"','"+format(datetime.datetime.now().strftime('%Y-%m-%d %T'))+"')")
    cursor.execute("INSERT INTO cello_outbound_data(pack_yn,inx,status,stat_cnt,ins_date) values ('Y',3,'일반출고 패킹완료','"+str(packing_CJ_Count)+"','"+format(datetime.datetime.now().strftime('%Y-%m-%d %T'))+"')")
    cursor.execute("INSERT INTO cello_outbound_data(pack_yn,inx,status,stat_cnt,ins_date) values ('N',4,'일반출고 패킹 미완료','"+str(nopacking_CJ_Count)+"','"+format(datetime.datetime.now().strftime('%Y-%m-%d %T'))+"')")
    cursor.execute("INSERT INTO cello_outbound_data(pack_yn,inx,status,stat_cnt,ins_date) values ('Y',5,'명품출고 패킹완료','"+str(btq_packing_Count)+"','"+format(datetime.datetime.now().strftime('%Y-%m-%d %T'))+"')")
    cursor.execute("INSERT INTO cello_outbound_data(pack_yn,inx,status,stat_cnt,ins_date) values ('N',6,'명품출고 패킹 미완료','"+str(btq_nopacking_Count)+"','"+format(datetime.datetime.now().strftime('%Y-%m-%d %T'))+"')")
    cursor.execute("INSERT INTO cello_outbound_data(pack_yn,inx,status,stat_cnt,ins_date) values ('Y',7,'명품일반출고 패킹완료','"+str(btq_CJ_packing_Count)+"','"+format(datetime.datetime.now().strftime('%Y-%m-%d %T'))+"')")
    cursor.execute("INSERT INTO cello_outbound_data(pack_yn,inx,status,stat_cnt,ins_date) values ('N',8,'명품일반출고 패킹 미완료','"+str(btq_CJ_nopacking_Count)+"','"+format(datetime.datetime.now().strftime('%Y-%m-%d %T'))+"')")
    
    con.commit()
    

    
def make_cello_data(reqDate,reqType):
        
    myToken = Common.getSlackToken()
    FolderYN = os.path.exists("D:\\m_project\\excelFile\\cello\\"+reqDate+"\\")
    if FolderYN==False:
        os.mkdir("D:\\m_project\\excelFile\\cello\\"+reqDate+"\\")

    pyear = int(reqDate[0:4])
    pmonth = int(reqDate[4:6])
    pday = int(reqDate[6:8])

    # pyear = int(2021)
    # pmonth = int(11)
    # pday = int(29)    
    # reqType='BTQDAY'


    header = getReqInfo.getSessionInfo().getCelloinfo()
    req_url = 'https://cello.samsungscl.com/cello/wms/integration/json/WMS_OBO_97_001' 
    timeCello = datetime.date(pyear, pmonth, pday)

    now = datetime.datetime.now()
    timeCello1 = timeCello + datetime.timedelta(days=-1)
    timeCello2 = timeCello1 + datetime.timedelta(days=1)
    param1 = "T15:00:00.000Z"
    param2 = "T14:59:59.000Z"
    
    os.putenv('NLS_LANG', '.UTF8')
    jsonData=[]
    jsonColData=[]
    startIndex =0
    endIndex =1
    cellonm =''
    returnData = []

    if reqType=='ALL':
        print('1')
        cellonm='전체조회'
        dataAll = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],"tr_read":{"readtype":2,"readindex":0,"readcount":1},"querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,"toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"","refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"","telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9","packYn":"","strrId":"","cartnNo":"","packScd":"","giTcd":"","trnsTcd":"","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"","dlvrySts":"","shiptoId":"","soNo":"","poNo":"","addrReqYn":"","waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"","salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"","prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},"protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}
        r = requests.post(req_url, headers=header,json=dataAll)
        rowCount = [json.loads(r.text)['rowcount']][0]
        
        if(rowCount!=0):
            forNum = math.ceil(rowCount/10000)
            for i in range(forNum):
                if(i==0) :
                    startIndex=0
                    endIndex=10000
                    dataAll = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],
                            "tr_read":{"readtype":2,"readindex":startIndex,"readcount":endIndex},
                            "querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,
                                        "toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"",
                                        "refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"",
                                        "telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9",
                                        "packYn":"","strrId":"","cartnNo":"","packScd":"","giTcd":"",
                                        "trnsTcd":"","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"",
                                        "dlvrySts":"","shiptoId":"","soNo":"","poNo":"","addrReqYn":"",
                                        "waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"",
                                        "salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"",
                                        "prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},
                                        "protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}

                    r = requests.post(req_url, headers=header, json=dataAll)
                    jsonColData = json.loads(r.text)['cols']
                    jsonData = json.loads(r.text)['rows']
                else :
                    startIndex+=10000
                    endIndex += 10000
                    dataAll = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],
                            "tr_read":{"readtype":2,"readindex":startIndex,"readcount":endIndex},
                            "querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,
                                        "toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"",
                                        "refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"",
                                        "telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9",
                                        "packYn":"","strrId":"","cartnNo":"","packScd":"","giTcd":"",
                                        "trnsTcd":"","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"",
                                        "dlvrySts":"","shiptoId":"","soNo":"","poNo":"","addrReqYn":"",
                                        "waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"",
                                        "salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"",
                                        "prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},
                                        "protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}
                    r = requests.post(req_url, headers=header, json=dataAll)
                    jsonData += json.loads(r.text)['rows']
            if(len(jsonData)!=0):
                excelData = pd.DataFrame(jsonData,columns=jsonColData)
                excelData.replace(np.nan,'',inplace=True)
                excelData['calpacking'] = np.where(excelData['totPackQty']==excelData['packQty'],'O','X')
                exportData=excelData[['shiptoId','trnsTcdNm','poNo','refDetlNo','invNo','packSnm','totPackQty','packQty','calpacking']]
                exportData.columns=['화주명','출고작업유형','오더번호','일련번호','송장번호','패킹상태','총패킹수량','패킹수량','패킹수량같음']
                
                # with pd.ExcelWriter(r'D:\\m_project\\excelFile\\cello\\'+reqDate+'\\'+reqDate+'_전체_'+now.strftime('%H%M%S')+'.xlsx') as writer:
                #     exportData.to_excel(writer,sheet_name="Sheet", index=None)
                #     autow(exportData,writer,sheet_name="Sheet",margin=2)
                    
                returnData = exportData

    elif reqType=='NORMAL':
        print('2')
        cellonm='일반출고'
        data = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],"tr_read":{"readtype":2,"readindex":0,"readcount":1},"querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,"toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"","refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"","telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9","packYn":"Y","strrId":"","cartnNo":"","packScd":"","giTcd":"","trnsTcd":"00","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"","dlvrySts":"","shiptoId":"MUSINSA","soNo":"","poNo":"","addrReqYn":"","waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"","salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"","prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},"protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}
        r = requests.post(req_url, headers=header,json=data)
        rowCount = [json.loads(r.text)['rowcount']][0]
        
        if(rowCount!=0):
            forNum = math.ceil(rowCount/10000)
            for i in range(forNum):
                if(i==0) :
                    startIndex=0
                    endIndex=10000
                    data = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],
                            "tr_read":{"readtype":2,"readindex":startIndex,"readcount":endIndex},
                            "querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,
                                        "toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"",
                                        "refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"",
                                        "telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9",
                                        "packYn":"Y","strrId":"","cartnNo":"","packScd":"","giTcd":"",
                                        "trnsTcd":"00","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"",
                                        "dlvrySts":"","shiptoId":"MUSINSA","soNo":"","poNo":"","addrReqYn":"",
                                        "waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"",
                                        "salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"",
                                        "prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},
                                        "protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}

                    r = requests.post(req_url, headers=header, json=data)
                    jsonColData = json.loads(r.text)['cols']
                    jsonData = json.loads(r.text)['rows']
                else :
                    startIndex+=10000
                    endIndex += 10000
                    data = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],
                            "tr_read":{"readtype":2,"readindex":startIndex,"readcount":endIndex},
                            "querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,
                                        "toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"",
                                        "refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"",
                                        "telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9",
                                        "packYn":"Y","strrId":"","cartnNo":"","packScd":"","giTcd":"",
                                        "trnsTcd":"00","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"",
                                        "dlvrySts":"","shiptoId":"MUSINSA","soNo":"","poNo":"","addrReqYn":"",
                                        "waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"",
                                        "salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"",
                                        "prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},
                                        "protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}
                    r = requests.post(req_url, headers=header, json=data)
                    jsonData += json.loads(r.text)['rows']
                if(len(jsonData)!=0):
                    excelData = pd.DataFrame(jsonData,columns=jsonColData)
                    excelData.replace(np.nan,'',inplace=True)
                    excelData['calpacking'] = np.where(excelData['totPackQty']==excelData['packQty'],'O','X')
                    exportData=excelData[['shiptoId','trnsTcdNm','poNo','refDetlNo','invNo','packSnm','totPackQty','packQty','calpacking']]
                    exportData.columns=['화주명','출고작업유형','오더번호','일련번호','송장번호','패킹상태','총패킹수량','패킹수량','패킹수량같음']
                    # exportData.to_excel(r'D:\\m_project\\excelFile\\cello\\'+reqDate+'\\'+reqDate+'_일반출고_'+now.strftime('%H%M%S')+'.xlsx',sheet_name='Sheet1', index=None)
                    
                    # with pd.ExcelWriter(r'D:\\m_project\\excelFile\\cello\\'+reqDate+'\\'+reqDate+'_일반출고_'+now.strftime('%H%M%S')+'.xlsx') as writer:
                    #     exportData.to_excel(writer,sheet_name="Sheet", index=None)
                    #     autow(exportData,writer,sheet_name="Sheet",margin=2)
                
                    returnData = exportData
    elif reqType=='DB':
        print('2-1')
        cellonm='DB저장'
        data = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],"tr_read":{"readtype":2,"readindex":0,"readcount":1},"querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,"toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"","refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"","telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9","packYn":"Y","strrId":"","cartnNo":"","packScd":"","giTcd":"","trnsTcd":"","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"","dlvrySts":"","shiptoId":"MUSINSA","soNo":"","poNo":"","addrReqYn":"","waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"","salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"","prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},"protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}
        r = requests.post(req_url, headers=header,json=data)
        
        rowCount = [json.loads(r.text)['rowcount']][0]
        
        if(rowCount!=0):
            forNum = math.ceil(rowCount/10000)
            
            for i in range(forNum):
                if(i==0) :
                    startIndex=0
                    endIndex=10000
                    data = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],"tr_read":{"readtype":2,"readindex":startIndex,"readcount":endIndex},"querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,"toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"","refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"","telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9","packYn":"Y","strrId":"","cartnNo":"","packScd":"","giTcd":"","trnsTcd":"","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"","dlvrySts":"","shiptoId":"MUSINSA","soNo":"","poNo":"","addrReqYn":"","waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"","salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"","prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},"protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}
                    r = requests.post(req_url, headers=header, json=data)
                    jsonColData = json.loads(r.text)['cols']
                    jsonData = json.loads(r.text)['rows']
   
                else :
                    startIndex+=10000
                    endIndex += 10000
                    data = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],"tr_read":{"readtype":2,"readindex":startIndex,"readcount":endIndex},"querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,"toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"","refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"","telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9","packYn":"Y","strrId":"","cartnNo":"","packScd":"","giTcd":"","trnsTcd":"","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"","dlvrySts":"","shiptoId":"MUSINSA","soNo":"","poNo":"","addrReqYn":"","waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"","salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"","prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},"protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}
                    
                    r = requests.post(req_url, headers=header, json=data)
                    jsonData += json.loads(r.text)['rows']


            if(len(jsonData)!=0):
                excelData = pd.DataFrame(jsonData,columns=jsonColData)
                excelData.replace(np.nan,'',inplace=True)
                excelData['calpacking'] = np.where(excelData['totPackQty']==excelData['packQty'],'O','X')
                exportData=excelData[['shiptoId','trnsTcdNm','poNo','refDetlNo','invNo','packSnm','totPackQty','packQty','calpacking']]
                # exportData.to_excel(r'D:\\m_project\\excelFile\\cello\\'+reqDate+'\\'+reqDate+'_일반출고_'+now.strftime('%H%M%S')+'.xlsx',sheet_name='Sheet1', index=None)
                # with pd.ExcelWriter(r'D:\\m_project\\excelFile\\cello\\'+reqDate+'\\'+reqDate+'_일반출고_'+now.strftime('%H%M%S')+'.xlsx') as writer:
                #     exportData.to_excel(writer,sheet_name="Sheet", index=None)
                #     autow(exportData,writer,sheet_name="Sheet",margin=2)
            
                returnData = exportData        
    elif reqType=='BTQDAY':  
        print('3')  
        cellonm='명품당일출고'
        data37 = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],"tr_read":{"readtype":2,"readindex":0,"readcount":1},"querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,"toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"","refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"","telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9","packYn":"","strrId":"","cartnNo":"","packScd":"","giTcd":"","trnsTcd":"37","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"","dlvrySts":"","shiptoId":"MUSINSA","soNo":"","poNo":"","addrReqYn":"","waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"","salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"","prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},"protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}
        r = requests.post(req_url, headers=header,json=data37)
        rowCount37 = [json.loads(r.text)['rowcount']][0]

        if(rowCount37!=0):            
            forNum = math.ceil(rowCount37/10000)
            for i in range(forNum):
                if(i==0) :
                    startIndex=0
                    endIndex=10000
                    data37 = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],
                            "tr_read":{"readtype":2,"readindex":startIndex,"readcount":endIndex},
                            "querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,
                                        "toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"",
                                        "refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"",
                                        "telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9",
                                        "packYn":"Y","strrId":"","cartnNo":"","packScd":"","giTcd":"",
                                        "trnsTcd":"37","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"",
                                        "dlvrySts":"","shiptoId":"MUSINSA","soNo":"","poNo":"","addrReqYn":"",
                                        "waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"",
                                        "salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"",
                                        "prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},
                                        "protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}

                    r = requests.post(req_url, headers=header, json=data37)
                    jsonColData = json.loads(r.text)['cols']
                    jsonData37 = json.loads(r.text)['rows']
                else :
                    startIndex+=10000
                    endIndex += 10000
                    data37 = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],
                            "tr_read":{"readtype":2,"readindex":startIndex,"readcount":endIndex},
                            "querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,
                                        "toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"",
                                        "refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"",
                                        "telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9",
                                        "packYn":"Y","strrId":"","cartnNo":"","packScd":"","giTcd":"",
                                        "trnsTcd":"37","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"",
                                        "dlvrySts":"","shiptoId":"MUSINSA","soNo":"","poNo":"","addrReqYn":"",
                                        "waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"",
                                        "salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"",
                                        "prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},
                                        "protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}
                    r = requests.post(req_url, headers=header, json=data37)
                    jsonData37 += json.loads(r.text)['rows']
            if(len(jsonData37)!=0):
                excelData37 = pd.DataFrame(jsonData37,columns=jsonColData)
                excelData37.replace(np.nan,'',inplace=True)
                excelData37['calpacking'] = np.where(excelData37['totPackQty']==excelData37['packQty'],'O','X')
                excelData37=excelData37[['shiptoId','trnsTcdNm','poNo','refDetlNo','invNo','packSnm','totPackQty','packQty','calpacking']]
                excelData37.columns=['화주명','출고작업유형','오더번호','일련번호','송장번호','패킹상태','총패킹수량','패킹수량','패킹수량같음']
                # excelData37.to_excel(r'D:\\m_project\\excelFile\\cello\\'+reqDate+'\\'+reqDate+'_명품당일배송_'+now.strftime('%H%M%S')+'.xlsx',sheet_name='Sheet1', index=None)
                
                # with pd.ExcelWriter(r'D:\\m_project\\excelFile\\cello\\'+reqDate+'\\'+reqDate+'_명품당일배송_'+now.strftime('%H%M%S')+'.xlsx') as writer:
                #     excelData37.to_excel(writer,sheet_name="Sheet", index=None)
                #     autow(excelData37,writer,sheet_name="Sheet",margin=2)
                returnData = excelData37        
    else:
        print('4')
        cellonm='명품택배'
        data38 = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],"tr_read":{"readtype":2,"readindex":0,"readcount":1},"querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,"toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"","refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"","telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9","packYn":"","strrId":"","cartnNo":"","packScd":"","giTcd":"","trnsTcd":"38","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"","dlvrySts":"","shiptoId":"MUSINSA","soNo":"","poNo":"","addrReqYn":"","waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"","salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"","prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},"protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}
        r = requests.post(req_url, headers=header,json=data38)
        rowCount38 = [json.loads(r.text)['rowcount']][0]

        if(rowCount38!=0):
            forNum = math.ceil(rowCount38/10000)
            for i in range(forNum):
                if(i==0) :
                    startIndex=0
                    endIndex=10000
                    data38 = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],
                            "tr_read":{"readtype":2,"readindex":startIndex,"readcount":endIndex},
                            "querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,
                                        "toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"",
                                        "refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"",
                                        "telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9",
                                        "packYn":"Y","strrId":"","cartnNo":"","packScd":"","giTcd":"",
                                        "trnsTcd":"38","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"",
                                        "dlvrySts":"","shiptoId":"MUSINSA","soNo":"","poNo":"","addrReqYn":"",
                                        "waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"",
                                        "salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"",
                                        "prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},
                                        "protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}
                    r = requests.post(req_url, headers=header, json=data38)
                    jsonColData = json.loads(r.text)['cols']
                    jsonData38 = json.loads(r.text)['rows']
                else :
                    startIndex+=10000
                    endIndex += 10000
                    data38 = {"dataset_id":"invoiceList","tr_add":[],"tr_delete":[],"tr_update":[],
                            "tr_read":{"readtype":2,"readindex":startIndex,"readcount":endIndex},
                            "querydata":{"fromExeEctDate":str(timeCello1.isoformat())+param1,
                                        "toExeEctDate":str(timeCello2.isoformat())+param2,"waveNo":"","shmptNo":"",
                                        "refNo":"","invNo":"","takePersonNm":"","itemCd":"","styleNo":"","brandNm":"",
                                        "telNo":"","hpNo":"","lalocStatScd":"0","lalocEndScd":"9",
                                        "packYn":"Y","strrId":"","cartnNo":"","packScd":"","giTcd":"",
                                        "trnsTcd":"38","fromActGiDate":None,"toActGiDate":None,"dlvryReqYn":"","carrCd":"",
                                        "dlvrySts":"","shiptoId":"MUSINSA","soNo":"","poNo":"","addrReqYn":"",
                                        "waveCreYn":"","salesNm":"","userCol17":"","buyerPoNo":"","lotAttrVal5":"","toteBox":"",
                                        "salesChannelIdList":[""],"prdtOptList":[""],"salesPriceFrom":"","salesPriceTo":"",
                                        "prdtCdList":[""],"prdtNm":"","partNoList":[""],"partOptNoList":[""]},
                                        "protocol_id":"__AUI_DSCOMM_PROTOCOL__","protocol_version":"0.0.4"}
                    r = requests.post(req_url, headers=header, json=data38)
                    jsonData38 += json.loads(r.text)['rows']
            if(len(jsonData38)!=0):
                excelData38 = pd.DataFrame(jsonData38,columns=jsonColData)
                excelData38.replace(np.nan,'',inplace=True)
                excelData38['calpacking'] = np.where(excelData38['totPackQty']==excelData38['packQty'],'O','X')
                excelData38=excelData38[['shiptoId','trnsTcdNm','poNo','refDetlNo','invNo','packSnm','totPackQty','packQty','calpacking']]
                excelData38.columns=['화주명','출고작업유형','오더번호','일련번호','송장번호','패킹상태','총패킹수량','패킹수량','패킹수량같음']
                # excelData38.to_excel(r'D:\\m_project\\excelFile\\cello\\'+reqDate+'\\'+reqDate+'_명품택배_'+now.strftime('%H%M%S')+'.xlsx',sheet_name='Sheet1', index=None)
                
                # with pd.ExcelWriter(r'D:\\m_project\\excelFile\\cello\\'+reqDate+'\\'+reqDate+'_명품택배_'+now.strftime('%H%M%S')+'.xlsx') as writer:
                #     excelData38.to_excel(writer,sheet_name="Sheet", index=None)
                #     autow(excelData38,writer,sheet_name="Sheet",margin=2)
                returnData = excelData38
    
    if  len(returnData)!=0:   
        Common.slack_message(myToken,"#logistics_manage_notice", cellonm+"_첼로파일 생성 ..완료 :cat-clap:") 
    
    return returnData
    