import io
import os
import sys
import json
import glob
import math
import time
import requests
import datetime
import pyautogui
import mysql.connector
import pandas as pd
import numpy as np
import smtplib
from io import StringIO
from bs4 import BeautifulSoup
from flask import Blueprint, request, render_template, flash, redirect, url_for,send_file
from flask import current_app as app
from app.module import dbModule,getReqInfo
from app.pyFile import Bizest,Moms,Cello,Common
from werkzeug.wrappers import response
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText            # 본문내용을 전송할 때 사용되는 모듈
from email.mime.multipart import MIMEMultipart  # 메시지를 보낼 때 메시지에 대한 모듈


 
excel= Blueprint('excel', __name__, url_prefix='/')
# 첫화면로딩
@excel.route('/excelDownload/', methods=['POST','GET'])
def excelDownload():
      auth = Common.getMacAddr()
      if auth=="Y":
            pdate = request.args.get('pDate')
            reTurnVal = Moms.select_moms_Excel() 
            reTurnVal1 = Cello.select_moms_cello_count()
            return render_template('/html/excelDownload.html',resultData=reTurnVal,resultDate=pdate,countData=reTurnVal1,authVal = auth)
      else:
            return render_template('/html/no-auth.html',authVal = auth)

# 조회
@excel.route('/excelSearch', methods=['POST','GET'])
def excelSearch():
      
      header = getReqInfo.getSessionInfo().getMomsinfo()
      now = datetime.datetime.now()
      nowDate = datetime.date(now.year, now.month, now.day)
      cls_date = nowDate.isoformat().replace('-','')
      url='https://moms.musinsa.com/api/grid/search/'   
      data = {'params':'{\"MENU_CD\":\"GI02_HEAD\",\"USR_ID\":\"heechan.lee@musinsa.com\",\"params\":{\"SPR_NM\":\"MUSINSA\",\"CLS_DATE\":[\"'+str(nowDate).replace("-","")+'\",\"'+str(nowDate).replace("-","")+'\"],\"CUT_OFF_NO\":\"\"},\"type\":\"click\",\"page\":1}'}
      jsonData= requests.post(url,headers=header,json=data).json()
      checkSearch = jsonData['rtnChk']
            
      if checkSearch==True:
            df = pd.DataFrame(jsonData['rtnData'])
            df1 = Moms.select_moms_Excel()     

            if len(df) != len(df1):      
                  df=df[['CUT_OFF_NO','CLS_DATE','CUT_SEQ','DOC_QTY']]
                  df = df.astype('str')

                  row = [tuple(x) for x in df.to_records(index=False)]
                  db_class = dbModule.Database()
                  sql = "DELETE  FROM moms_outbound_data WHERE CLS_DATE='"+str(cls_date)+"'"
                  db_class.execute(sql)
                  db_class.commit()

                  sql1 = "INSERT INTO moms_outbound_data(CUT_OFF_NO,CLS_DATE,CUT_SEQ,DOC_QTY,INS_DATE) values (%s,%s,%s,%s,'"+format(datetime.datetime.now().strftime('%Y-%m-%d %T'))+"')"
                  db_class.executemany(sql1,row)
                  db_class.commit()
                  
                  req_url = 'https://bizest.musinsa.com/ho/order/ord36'
                  r = requests.post(req_url+ str('?API_KEY=d1869a20cd1a6f12c42d41f714df3325&API_USER_ID=mss_632'))
                  soup = BeautifulSoup(r.text,'lxml')
                  select = soup.find("select",attrs={ "name":"S_DLV_SERIES_NO"})
                  list = select.findAll('option')

                  for l in list:
                        if l.text in df['CUT_OFF_NO'].to_list():
                              sql2 = "UPDATE moms_outbound_data set BZ_YN = 'Y' WHERE CUT_OFF_NO='"+l.text+"'"
                              db_class.execute(sql2)
                  db_class.commit()

                  
                  # for l in list:
                  #       if l.text in '2022021814_MUSINSA_BT1':
                  #             print(l)
                        
                  
                  
      return redirect(url_for('excel.excelDownload',pDate=""))

# FTP폴더에 한꺼번에 다운받기
@excel.route('/makeExcel', methods=['POST','GET'])
def makeExcel():
      
      resultVal = False
      serialNo = request.args.get('serialNo')
      clsdate = request.args.get('clsdate')
      cutseq = request.args.get('cutseq')

      FolderYN = os.path.exists("D:\\m_project\\excelFile\\moms\\"+clsdate+"\\")
      if FolderYN==False:
            os.mkdir("D:\\m_project\\excelFile\\moms\\"+clsdate+"\\")

      url='https://moms.musinsa.com/api/grid/search/'   
      
      myToken = Common.getSlackToken()
      header = getReqInfo.getSessionInfo().getMomsinfo()
      user_id='heechan.lee@musinsa.com'
     
      excelData1 =[]
      excelData2 =[]
      excelData3 =[]
      excelData4 =[]
      excelData5 =[]
      

      bzyn ='N'
      req_url = 'https://bizest.musinsa.com/ho/order/ord36'
      r = requests.post(req_url+ str('?API_KEY=d1869a20cd1a6f12c42d41f714df3325&API_USER_ID=mss_632'))
      soup = BeautifulSoup(r.text,'lxml')
      select = soup.find("select",attrs={ "name":"S_DLV_SERIES_NO"})
      list = select.findAll('option')

      for l in list:
            if serialNo in l.text:
                  bzyn ='Y'
      
      #데이터 구분
      if "BT" in serialNo:
            outKinds = ' 명품 '       
      else:
            outKinds = ' 무신사 '

      # 총주문
      data1 = {'params':'{\"params\":{\"TAB_IDX\":1,\"CLS_DATE\":\"'+clsdate+'\",\"CUT_SEQ\":"'+cutseq+'",\"CUT_OFF_NO\":\"'+serialNo+'\",\"SPR_NM\":\"MUSINSA\"},\"MENU_CD\":\"GI02_ITEM1\",\"USR_ID\":\"'+user_id+'\"}'}
      jsonData1= requests.post(url,headers=header,json=data1).json()
      totalCnt = 0
      if jsonData1['rtnChk']!=False:
            excelData1 = pd.DataFrame(jsonData1['rtnData'])
            excelData1[["CUT_OFF_NO","ORD_NO","ORD_OPT_NO","PROC_NM","ORD_NM","TRS_NM","TRS_ZIP","TRS_ADDR","TRS_ADDR2","TRS_ADDR3","TRS_PHONE","TRS_MOBILE","GDS_COMBINE","GDS_LOCATION","GDS_OPT","ORD_QTY","GDS_TYPE","BRD_NM","GIFT","TRS_MSG","STL_NO","BARCODE","TRS_INVOICE_NO"]].to_excel(r'D:\\m_project\\excelFile\\moms\\'+clsdate+'\\' + str(serialNo)+'_'+cutseq+'_'+outKinds+'총주문.xlsx',sheet_name='Sheet1', index=None)
            totalCnt = len(excelData1)

      # 할당
      data2 = {"params":'{\"params\":{\"TAB_IDX\":2,\"CLS_DATE\":\"'+clsdate+'\",\"CUT_SEQ\":"'+cutseq+'",\"CUT_OFF_NO\":\"'+serialNo+'\",\"SPR_NM\":\"MUSINSA\"},\"MENU_CD\":\"GI02_ITEM1\",\"USR_ID\":\"'+user_id+'\"}'}
      jsonData2= requests.post(url,headers=header,json=data2).json()
      invCnt = 0
      if jsonData2['rtnChk']!=False:
            excelData2 = pd.DataFrame(jsonData2['rtnData'])
            excelData2[["CUT_OFF_NO","ORD_NO","ORD_OPT_NO","PROC_NM","ORD_NM","TRS_NM","TRS_ZIP","TRS_ADDR","TRS_ADDR2","TRS_ADDR3","TRS_PHONE","TRS_MOBILE","GDS_COMBINE","GDS_LOCATION","GDS_OPT","ORD_QTY","GDS_TYPE","BRD_NM","GIFT","TRS_MSG","STL_NO","BARCODE","TRS_INVOICE_NO"]].to_excel(r'D:\\m_project\\excelFile\\moms\\'+clsdate+'\\' + str(serialNo)+'_'+cutseq+'_'+outKinds+'할당.xlsx',sheet_name='Sheet1', index=None)
            invCnt = len(excelData2)

      # 미할당
      data3 = {'params':'{\"params\":{\"TAB_IDX\":3,\"CLS_DATE\":\"'+clsdate+'\",\"CUT_SEQ\":"'+cutseq+'",\"CUT_OFF_NO\":\"'+serialNo+'\",\"SPR_NM\":\"MUSINSA\"},\"MENU_CD\":\"GI02_ITEM1\",\"USR_ID\":\"'+user_id+'\"}'}
      jsonData3= requests.post(url,headers=header,json=data3).json()

      noinvCnt = 0
      if jsonData3['rtnChk']!=False:
            excelData3 = pd.DataFrame(jsonData3['rtnData'])
            excelData3[["CUT_OFF_NO","ORD_NO","ORD_OPT_NO","PROC_NM","ORD_NM","TRS_NM","TRS_ZIP","TRS_ADDR","TRS_ADDR2","TRS_ADDR3","TRS_PHONE","TRS_MOBILE","GDS_COMBINE","GDS_LOCATION","GDS_OPT","ORD_QTY","GDS_TYPE","BRD_NM","GIFT","TRS_MSG","STL_NO","BARCODE","TRS_PASS"]].to_excel(r'D:\\m_project\\excelFile\\moms\\'+clsdate+'\\' + str(serialNo)+'_'+cutseq+'_'+outKinds+'미할당.xlsx',sheet_name='Sheet1', index=None)
            noinvCnt = len(excelData3)

      # 이상발생
      data4 = {'params':'{\"params\":{\"TAB_IDX\":4,\"CLS_DATE\":\"'+clsdate+'\",\"CUT_SEQ\":"'+cutseq+'",\"CUT_OFF_NO\":\"'+serialNo+'\",\"SPR_NM\":\"MUSINSA\"},\"MENU_CD\":\"GI02_ITEM1\",\"USR_ID\":\"'+user_id+'\"}'}
      jsonData4 = requests.post(url,headers=header,json=data4).json()

      emerCnt = 0
      if jsonData4['rtnChk']!=False:
            excelData4 = pd.DataFrame(jsonData4['rtnData'])
            excelData4[["CUT_OFF_NO","ORD_NO","ORD_OPT_NO","PROC_NM","ORD_NM","TRS_NM","TRS_ZIP","TRS_ADDR","TRS_ADDR2","TRS_ADDR3","TRS_PHONE","TRS_MOBILE","GDS_COMBINE","GDS_LOCATION","GDS_OPT","ORD_QTY","GDS_TYPE","BRD_NM","GIFT","TRS_MSG","STL_NO","BARCODE"]].to_excel(r'D:\\m_project\\excelFile\\moms\\'+clsdate+'\\' + str(serialNo)+'_'+cutseq+'_'+outKinds+'이상발생.xlsx',sheet_name='Sheet1', index=None)
            emerCnt = len(excelData4)
            
      # 첼로
      data5 = {'params':'{\"params\":{\"TAB_IDX\":5,\"CLS_DATE\":\"'+clsdate+'\",\"CUT_SEQ\":"'+cutseq+'",\"CUT_OFF_NO\":\"'+serialNo+'\",\"SPR_NM\":\"MUSINSA\"},\"MENU_CD\":\"GI02_ITEM1\",\"USR_ID\":\"'+user_id+'\"}'}
      jsonData5= requests.post(url,headers=header,json=data5).json()
      celloCnt = 0
      if jsonData5['rtnChk']!=False:
            excelData5 = pd.DataFrame(jsonData5['rtnData'])
            # print('갯수비교............할당갯수:',len(excelData2),'   첼로데이터갯수:',len(excelData5))
            while len(excelData2) != len(excelData5):
                  time.sleep(5)
                  jsonData5= requests.post(url,headers=header,json=data5).json()
                  excelData5 = pd.DataFrame(jsonData5['rtnData'])

            excelData5[["DOCUMENT_NO","ORD_TYPE","ORD_PART_ID","SBU_ID","FORWARDER_ID","SERVICE_TYPE","DST","BIZ_TYPE","ORIGIN_DO_NO","INCOTERMS","SI_CD","REASON_CD","URGENT","SHIPPING_POINT","PLANT_CD","PGI_DATE","PGI_TIME","DLV_ORD_NO","DLV_DATE","DLV_TIME","DLV_EXPECT_DATE","LT_YN","EL_YN","HP_YN","OG_YN","FROM_NODE_CD","FROM_CITY","FROM_NATION","FROM_ZIP","FROM_ADDRESS","ETDDATE","ETDTIME","TN_CD","TO_CITY","TO_NATION","TO_ZIP","TO_ADDRESS","ETADATE","ETATIME","SCC","MI_CD_CHK_YN","ITEM_CD","ITEM_NM","ITEM_NO","SERIAL_NO","ITEM_PRICE","ITEM_CC","PO_NO","PO_ITEM_NO","PODATE","POTIME","SO_NO","SI_ITEM_NO","DIVISION_CD","QTY","UNIT","PACKING_QTY","UNIT2","GW","UNIT3","NW","UNIT4","VL","UNIT5","CWT","UNIT6","SL_CD","SL_NM","PL_NO","VAL_DT","PRO_DT","LOT_ATTR1","LOT_ATTR2","LOT_ATTR3","LOT_ATTR4","LOT_ATTR5","LOT_ATTR6","REMARK","USR_COL1","USR_COL2","USR_COL3","USR_COL4","USR_COL5","USR_COL6","USR_COL7","USR_COL8","USR_COL9","USR_COL10","WORK_TYPE","WORK_SUB_TYPE","BACK_ORD_YN","PARTIAL_ALLOC_YN","PARTIAL_GI_YN","ORG_TYPE","ORG_CD","ORD_NM","ORD_TEL","FAX","ORD_ADDR","ORD_ADDR2","ORD_ADDR3","ORD_ADDR4","ORD_ADDR5","NATION_CD","MOBILE","ORDER_REMARK"]].to_excel(r'D:\\m_project\\excelFile\\moms\\'+clsdate+'\\' + str(serialNo)+'_'+cutseq+'_'+outKinds+'첼로폼.xlsx',sheet_name='Sheet1', index=None)
            celloCnt = len(excelData5)
            Common.slack_message(myToken,"#logistics_manage_notice", serialNo+"  "+outKinds+" 파일생성...완료 :cat-clap:") 

      db_class = dbModule.Database()
      sql = "insert into moms_excel_log(CUT_OFF_NO,CLS_DATE,CUT_SEQ,TOTAL,INV,NO_INV,EMER,CELLO,BZ_YN,MAKE_YN) VALUES ('"+str(serialNo)+"','"+str(clsdate)+"','"+str(cutseq)+"','"+str(totalCnt)+"','"+str(invCnt)+"','"+str(noinvCnt)+"','"+str(emerCnt)+"','"+str(celloCnt)+"','"+str(bzyn)+"','Y')"
      
      db_class.execute(sql)
      db_class.commit()

      return redirect(url_for('excel.excelDownload',pDate=""))

# 각각다운받기
@excel.route('/downExcel', methods=['POST','GET'])
def downExcel():
      type =request.args.get('type')
      serialNo =request.args.get('serialNo')
      url='https://moms.musinsa.com/api/grid/search/'   
      user_id='heechan.lee@musinsa.com'
      header = getReqInfo.getSessionInfo().getMomsinfo()
      momsSerialInfo = Common.getMomsCutoffinfo(serialNo)
      clsdate = momsSerialInfo[0]
      cutseq = momsSerialInfo[1]
      strIO = io.BytesIO()
      
      if type =='total':
            # 총주문
            data1 = {'params':'{\"params\":{\"TAB_IDX\":1,\"CLS_DATE\":\"'+clsdate+'\",\"CUT_SEQ\":'+cutseq+',\"CUT_OFF_NO\":\"'+serialNo+'\",\"SPR_NM\":\"MUSINSA\"},\"MENU_CD\":\"GI02_ITEM1\",\"USR_ID\":\"'+user_id+'\"}'}
            jsonData1= requests.post(url,headers=header,json=data1).json()
            file_name = str(serialNo)+'_총주문.xlsx'
            excelData1 = pd.DataFrame(jsonData1['rtnData'])
            excelData2 = excelData1[["CUT_OFF_NO","ORD_NO","ORD_OPT_NO","PROC_NM","ORD_NM","TRS_NM","TRS_ZIP","TRS_ADDR","TRS_PHONE","TRS_MOBILE","GDS_COMBINE","GDS_LOCATION","GDS_OPT","ORD_QTY","GDS_TYPE","BRD_NM","GIFT","TRS_MSG","STL_NO","BARCODE","TRS_INVOICE_NO"]]
      elif type =='inv':
            # 할당
            data1 = {'params':'{\"params\":{\"TAB_IDX\":2,\"CLS_DATE\":\"'+clsdate+'\",\"CUT_SEQ\":'+cutseq+',\"CUT_OFF_NO\":\"'+serialNo+'\",\"SPR_NM\":\"MUSINSA\"},\"MENU_CD\":\"GI02_ITEM1\",\"USR_ID\":\"'+user_id+'\"}'}
            jsonData1= requests.post(url,headers=header,json=data1).json()
            file_name = str(serialNo)+'_할당.xlsx'
            excelData1 = pd.DataFrame(jsonData1['rtnData'])
            excelData2 = excelData1[["CUT_OFF_NO","ORD_NO","ORD_OPT_NO","PROC_NM","ORD_NM","TRS_NM","TRS_ZIP","TRS_ADDR","TRS_PHONE","TRS_MOBILE","GDS_COMBINE","GDS_LOCATION","GDS_OPT","ORD_QTY","GDS_TYPE","BRD_NM","GIFT","TRS_MSG","STL_NO","BARCODE","TRS_INVOICE_NO"]]
      elif type =='noinv':
            # 미할당
            data1 = {'params':'{\"params\":{\"TAB_IDX\":3,\"CLS_DATE\":\"'+clsdate+'\",\"CUT_SEQ\":'+cutseq+',\"CUT_OFF_NO\":\"'+serialNo+'\",\"SPR_NM\":\"MUSINSA\"},\"MENU_CD\":\"GI02_ITEM1\",\"USR_ID\":\"'+user_id+'\"}'}
            jsonData1= requests.post(url,headers=header,json=data1).json()
            file_name = str(serialNo)+'_미할당.xlsx'
            excelData1 = pd.DataFrame(jsonData1['rtnData'])
            excelData2 = excelData1[["CUT_OFF_NO","ORD_NO","ORD_OPT_NO","PROC_NM","ORD_NM","TRS_NM","TRS_ZIP","TRS_ADDR","TRS_PHONE","TRS_MOBILE","GDS_COMBINE","GDS_LOCATION","GDS_OPT","ORD_QTY","GDS_TYPE","BRD_NM","GIFT","TRS_MSG","STL_NO","BARCODE","TRS_PASS"]]
      elif type =='cello':
            # 첼로
            data1 = {'params':'{\"params\":{\"TAB_IDX\":5,\"CLS_DATE\":\"'+clsdate+'\",\"CUT_SEQ\":'+cutseq+',\"CUT_OFF_NO\":\"'+serialNo+'\",\"SPR_NM\":\"MUSINSA\"},\"MENU_CD\":\"GI02_ITEM1\",\"USR_ID\":\"'+user_id+'\"}'}
            jsonData1= requests.post(url,headers=header,json=data1).json()
            file_name = str(serialNo)+'_첼로폼.xlsx'
            excelData1 = pd.DataFrame(jsonData1['rtnData'])
            excelData2 = excelData1[["DOCUMENT_NO","ORD_TYPE","ORD_PART_ID","SBU_ID","FORWARDER_ID","SERVICE_TYPE","DST","BIZ_TYPE","ORIGIN_DO_NO","INCOTERMS","SI_CD","REASON_CD","URGENT","SHIPPING_POINT","PLANT_CD","PGI_DATE","PGI_TIME","DLV_ORD_NO","DLV_DATE","DLV_TIME","DLV_EXPECT_DATE","LT_YN","EL_YN","HP_YN","OG_YN","FROM_NODE_CD","FROM_CITY","FROM_NATION","FROM_ZIP","FROM_ADDRESS","ETDDATE","ETDTIME","TN_CD","TO_CITY","TO_NATION","TO_ZIP","TO_ADDRESS","ETADATE","ETATIME","SCC","MI_CD_CHK_YN","ITEM_CD","ITEM_NM","ITEM_NO","SERIAL_NO","ITEM_PRICE","ITEM_CC","PO_NO","PO_ITEM_NO","PODATE","POTIME","SO_NO","SI_ITEM_NO","DIVISION_CD","QTY","UNIT","PACKING_QTY","UNIT2","GW","UNIT3","NW","UNIT4","VL","UNIT5","CWT","UNIT6","SL_CD","SL_NM","PL_NO","VAL_DT","PRO_DT","LOT_ATTR1","LOT_ATTR2","LOT_ATTR3","LOT_ATTR4","LOT_ATTR5","LOT_ATTR6","REMARK","USR_COL1","USR_COL2","USR_COL3","USR_COL4","USR_COL5","USR_COL6","USR_COL7","USR_COL8","USR_COL9","USR_COL10","WORK_TYPE","WORK_SUB_TYPE","BACK_ORD_YN","PARTIAL_ALLOC_YN","PARTIAL_GI_YN","ORG_TYPE","ORG_CD","ORD_NM","ORD_TEL","FAX","ORD_ADDR","ORD_ADDR2","ORD_ADDR3","ORD_ADDR4","ORD_ADDR5","NATION_CD","MOBILE","ORDER_REMARK"]]
      
      excel_writer = pd.ExcelWriter(strIO,engine="xlsxwriter")
      excelData2.to_excel(excel_writer,sheet_name='sheet1', index=None)
      excel_writer.save()
      excel_data = strIO.getvalue()
      strIO.seek(0)
                  
      return send_file(strIO,attachment_filename=file_name, as_attachment=True)


# @excel.route('/reload_all', methods=['POST','GET'])
# def reload_all():
      
#       # Bizest.get_bizest_data()
#       # Bizest.update_count_bizest()
#       # Moms.update_count_moms()
#       # Cello.upload_cello_data()
#       # Cello.update_count_cello()
      
#       return redirect(url_for('excel.index'))

@excel.route('/celloAll/<cDate>-<cType>', methods=['POST','GET'])
def celloAll(cDate,cType):

      if cType=='ALL':
            file_name = str(cDate)+'_첼로_전체.xlsx'
      elif cType=='NORMAL':
            file_name = str(cDate)+'_첼로_일반택배.xlsx'
      elif cType=='BTQDAY':
            file_name = str(cDate)+'_첼로_명품_당일배송.xlsx'
      else:
            file_name = str(cDate)+'_첼로_명품_택배.xlsx'

      returnVal = Cello.make_cello_data(cDate,cType)
      
      if len(returnVal)!=0:
            strIO = io.BytesIO()
            excel_writer = pd.ExcelWriter(strIO,engine="xlsxwriter")
            returnVal.to_excel(excel_writer,sheet_name='sheet1', index=None)
            excel_writer.sheets['sheet1'].set_column('A:B',12)
            excel_writer.sheets['sheet1'].set_column('C:E',20)
            excel_writer.sheets['sheet1'].set_column('F:H',12)
            excel_writer.save()
            strIO.seek(0)                  
            return send_file(strIO,attachment_filename=file_name, as_attachment=True)
            
      else:
            flash("조회된 데이터가 없습니다.")
            return redirect(url_for('excel.excelDownload',pDate=cDate))    

@excel.route('/celloSaveDB/<cDate>', methods=['POST','GET'])
def celloSaveDB(cDate):
      
      returnVal = Cello.make_cello_data(cDate,'DB')
      
      if len(returnVal)==0:
            flash('첼로 데이터가 없습니다.')            
      else:
            db_class = dbModule.Database()
            sql = "DELETE  FROM cello_request_data"
            db_class.execute(sql)
            db_class.commit()
            
            print('cDate======================',cDate)

            rows = [tuple(x) for x in returnVal.to_records(index=False)]
            sql1 = "INSERT INTO cello_request_data(spr_nm,trs_type,ord_no,ord_opt_no,invoice_no,packing_yn,total_qty,packing_qty,qty_yn,ins_date) values (trim(%s),trim(%s),trim(%s),trim(%s),trim(%s),trim(%s),trim(%s),trim(%s),trim(%s),"+cDate+")"
            for i in rows:
                  db_class.execute(sql1,i)
            db_class.commit()

            
            sql2 = "SELECT COUNT(*) FROM cello_request_data"
            reCount = db_class.executeOne(sql2)[0]

            if len(returnVal) == reCount:
                  flash("데이터를 저장하였습니다.")
            else:
                  sql = "DELETE  FROM cello_request_data"
                  db_class.execute(sql)
                  db_class.commit()
                  flash("데이터 저장에 실패했습니다.")


      return redirect(url_for('excel.excelDownload',pDate=cDate))  


@excel.route('/inputsongjang', methods=['POST','GET'])
def inputsongjang():
      if request.method=='POST':
            value = request.form['textarea1'].split('\r')
            
            row =[]
            for x in value:
                  y=x.replace('\n','')
                  if len(y) !=0:
                      row.append(y)
            
            df = pd.DataFrame(row)
            print(df)


            row = [tuple(x) for x in df.to_records(index=False)]  
                        
            db_class = dbModule.Database()
            sql = "DELETE  FROM cp_data1"
            db_class.execute(sql)
            db_class.commit()

            sql1 = "INSERT INTO cp_data1(ORD_OPT_NO) values (trim(%s))"
            db_class.executemany(sql1,row)
            db_class.commit()

      return redirect(url_for('excel.excelDownload',pDate=""))
      
@excel.route('/inputsongjang1', methods=['POST','GET'])
def inputsongjang1():
      if request.method=='POST':
            value = request.form['textarea2'].split('\r')
            row =[]
            for x in value:
                  y = x.replace('\n','')
                  if len(y) !=0:
                      z=y.split('\t')
                      row.append(tuple(z))
            
            df = pd.DataFrame(row)
                       
            row = [tuple(x) for x in df.to_records(index=False)]  
                        
            db_class = dbModule.Database()
            sql = "DELETE  FROM cp_data2"
            db_class.execute(sql)
            db_class.commit()

            sql1 = "INSERT INTO cp_data2(ORD_OPT_NO,SEND_CUST_NO) values (trim(%s),trim(%s))"
            db_class.executemany(sql1,row)
            db_class.commit()

      return redirect(url_for('excel.excelDownload',pDate=""))

@excel.route('/deleteExcelFile', methods=['POST','GET'])
def deleteExcelFile():
      serialNo = request.args.get('serialNo')
      clsdate = request.args.get('clsdate')
      cutseq = request.args.get('cutseq')

      db_class = dbModule.Database()
      sql1 = "DELETE  FROM moms_excel_log WHERE CUT_OFF_NO = '"+str(serialNo)+"' and CLS_DATE='"+str(clsdate)+"' and CUT_SEQ = '"+str(cutseq)+"' "
      sql2 = "DELETE  FROM moms_outbound_data WHERE CUT_OFF_NO = '"+str(serialNo)+"' and CLS_DATE='"+str(clsdate)+"' and CUT_SEQ = '"+str(cutseq)+"' "
      db_class.execute(sql1)
      # db_class.execute(sql2)
      db_class.commit()
      
      files = glob.glob('D:\\m_project\\excelFile\\moms\\'+str(clsdate)+'\\'+str(serialNo)+'_'+str(cutseq)+'*')
      for f in files:
            os.remove(f)

      return redirect(url_for('excel.excelDownload',pDate=""))

@excel.route('/excelupload', methods=['POST'])
def excelupload():
      
      if request.method=="POST":
            db_class = dbModule.Database()
            sql = "DELETE  FROM moms_request_data"
            db_class.execute(sql)
            db_class.commit()
                        
            file = request.files['excelUpload']
            if file.filename !='':
                  df = pd.read_excel(file)
                  df.replace(np.nan, '', inplace=True)
                  df = df.astype(str)
                  df1= df[['CUT_OFF_NO','ORD_NO','ORD_OPT_NO','PROC_NM','ORD_NM','TRS_NM','TRS_ZIP','TRS_ADDR','TRS_ADDR2','TRS_ADDR3','TRS_PHONE','TRS_MOBILE','GDS_COMBINE','GDS_LOCATION','GDS_OPT','ORD_QTY','GDS_TYPE','BRD_NM','GIFT','TRS_MSG','STL_NO','BARCODE']]
                  rows = [tuple(x) for x in df1.to_records(index=False)]
                  
                  sql1 = "INSERT INTO moms_request_data(CUT_OFF_NO,ORD_NO,ORD_OPT_NO,PROC_NM,ORD_NM,TRS_NM,TRS_ZIP,TRS_ADDR,TRS_ADDR2,TRS_ADDR3,TRS_PHONE,TRS_MOBILE,GDS_COMBINE,GDS_LOCATION,GDS_OPT,ORD_QTY,GDS_TYPE,BRD_NM,GIFT,TRS_MSG,STL_NO,BARCODE,FILE_NAME) values (trim(%s),trim(%s),trim(%s),trim(%s),substr(trim(%s),1,240),trim(%s),trim(%s),trim(%s),trim(%s),trim(%s),trim(%s),trim(%s),trim(%s),trim(%s),trim(%s),trim(%s),trim(%s),trim(%s),trim(%s),substr(trim(%s),1,240),trim(%s),replace(trim(%s),' ',''),'"+file.filename+"')"
                  
                  for i in rows:
                        db_class.execute(sql1,i)
                  
                  db_class.commit()
                  
                  sql2 = "SELECT COUNT(*) FROM moms_request_data"
                  reCount = db_class.executeOne(sql2)[0]

                  if len(df) == reCount:
                        flash("데이터를 저장하였습니다.")
                  else:
                        sql = "DELETE  FROM moms_request_data"
                        db_class.execute(sql)
                        db_class.commit()
                        flash("데이터 저장에 실패했습니다.")
                  
                  return redirect(url_for('excel.excelDownload',pDate=""))
            else:
                  flash("엑셀파일을 업로드해주세요.")                  
                  return redirect(url_for('excel.excelDownload',pDate=""))

@excel.route('/sendExcelMail', methods=['POST','GET'])
def sendExcelMail():
      
      serialNo = request.args.get('serialNo')
      clsdate = request.args.get('clsdate')
      cutseq = request.args.get('cutseq')
      celloCnt = request.args.get('celloCnt')
      
      if "BT" in serialNo:
            outKinds = ' 명품 '       
      else:
            outKinds = ' 무신사 '
      
      typeNm = '첼로폼'
      
    
      # 메일전송
      pw = 'xogecibttjxhqyqv'
      email = 'musinsamomsmail@gmail.com'
      smtp = smtplib.SMTP('smtp.gmail.com', 587)
      smtp.starttls()
      smtp.login(email, pw)

      msg = MIMEMultipart()
      msg['From'] = 'MUSINSALOGISTICS'
      if outKinds==' 명품 ':
            msg['Subject'] = ' 무신사 명품 (' + serialNo + ')  출고파일 전송'
      else:
            msg['Subject'] = ' 무신사 (' + serialNo + ')  출고파일 전송'
      
      addText = '할당 주문건  ' +celloCnt+ '건입니다.'
      
      # text msg
      part = MIMEText(
            '<table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse; max-width: 872px;" width="100%"><tbody><tr><td height="22"><p>안녕하십니까?</p><p>본 메일은 무신사 물류운영팀에서 출고 담당자에게 자동으로 전송되고 있습니다.</p><p>&nbsp;</p><p><strong><span style="font-size:16px;">* ' + str(serialNo) + '차수 출고 파일을 전달 드립니다 확인부탁드립니다.</span></strong></p><p><strong><span style="font-size:16px;">' + addText + '</span></strong></p><p>&nbsp;</p></td></tr><tr><td height="22" style="border-top-color: rgb(0, 0, 0); border-top-width: 1px; border-top-style: solid;">&nbsp;</td></tr><tr></tr><tr><td height="4">&nbsp;</td></tr><tr></tr><tr><td height="35">&nbsp;</td></tr><tr><td height="15">&nbsp;</td></tr><tr><td height="15" style="border-top-color: rgb(248, 248, 248); border-top-width: 1px; border-top-style: solid;">&nbsp;</td></tr><tr><td>※ 본 이메일에는 법률상 공개가 금지되거나 공개하여서는 안 되는 비밀정보가 포함되어 있을 수 있습니다. 본 이메일을 받으신 분이 해당 수신인이 아니거나 또는 본 이메일을 해당 수신인에게 전달할 책임이 있는 직원 또는 대리인이 아닌 경우, 본 이메일을 전파 또는 배포하거나, 복사하는 것은 엄격히 금지되어 있습니다. 만일 본 이메일이 잘못 전송되었을 경우에는 즉시 발신인에게 알려주시고 귀하의 컴퓨터에서 본 이메일을 삭제하여 주시기 바랍니다. 이 메일의 발신인은 컴퓨터 바이러스 등으로 인하여 발생할 수 있는 문제에 대하여 책임을 부담하지 않습니다. 메일의 수신인께서도 바이러스의 존재 여부를 사전에 검사하시기 바랍니다.</td></tr></tbody></table>',
            'html')
      msg.attach(part)

      if str(celloCnt) != '0':
            att1 = MIMEApplication(
                  open(r'D:\\m_project\\excelFile\\moms\\'+clsdate+'\\' + str(serialNo)+'_'+cutseq+'_'+outKinds+typeNm+'.xlsx', 'rb').read())
            att1.add_header('Content-Disposition', 'attachment', filename=str(serialNo)+outKinds+'첼로폼.xlsx')
            msg.attach(att1)

      # 받을 사람
      rec_list =['boram.yu@partner.samsung.com','hyejun.jeon@partner.samsung.com','ricky.hwang@samsung.com','hyejung2.cho@partner.samsung.com','sungwoo1.ahn@samsung.com','ysm@musinsalogistics.co.kr','sungjin.go@musinsalogistics.co.kr','ksh2@musinsalogistics.co.kr','pdj@musinsalogistics.co.kr','hoonkyeom.song@musinsalogistics.co.kr','heechan.lee@musinsalogistics.co.kr','sys@musinsalogistics.co.kr']
      # rec_list =['sungjin.go@musinsalogistics.co.kr','reconk2@gmail.com']
      rec = ','.join(rec_list)
      msg['To'] = rec

      smtp.sendmail(msg['From'], rec_list, msg.as_string())
      smtp.quit()  
      
      flash("메일을 전송하였습니다.")
      return redirect(url_for('excel.excelDownload',pDate=""))     
    
     
    
