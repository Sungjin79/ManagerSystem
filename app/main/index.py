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
 
main= Blueprint('main', __name__, url_prefix='/')
 
@main.route('/', methods=['POST','GET'])
def index():
      return redirect(url_for('excel.excelDownload',pDate=''))
      # reTurnVal = ['0','0','0','0','0','0','0','0','0','0']   #Bizest.select_index()
      # reTurnVal1 = ['','']  #Bizest.select_BZ_data()
      # reTurnMomsVal = [('','','0','0','0','0','0','','0','0'),('','','0','0','0','0','0','','0','0')]   #Moms.select_moms_index()
      # reTurnMomsVal1 = ['N','','0','0','0','0','','0' ]  #Moms.select_moms_data()
      # reTurnCelloVal = ['','','','','','','','','','','','','','','']  #Cello.select_cello_index()
      # reTurnCelloVal1 = ['','',''] #Cello.select_cello_data()

      # return render_template('/html/index.html',resultData=reTurnVal,
      #                                           resultMomsData1=reTurnMomsVal[0],
      #                                           resultMomsData2=reTurnMomsVal[1],
      #                                           resultCelloData=reTurnCelloVal,
      #                                           BZTableData = reTurnVal1,
      #                                           momsTableData = reTurnMomsVal1,
      #                                           celloTableData =reTurnCelloVal1
      #                                           )

@main.route('/downExcel2', methods=['POST','GET'])
def downExcel2():
      type =request.args.get('type')
      serialNo = request.args.get('serialNo')
      clsdate = request.args.get('clsdate')
      cutseq = request.args.get('cutseq')
      
      if "BT" in serialNo:
            outKinds = ' 명품 '       
      else:
            outKinds = ' 무신사 '
      
      if type =='total':
            # 총주문
            typeNm = '총주문'
            
      elif type =='inv':
            # 할당
            typeNm = '할당'
            
      elif type =='noinv':
            # 미할당
            typeNm = '미할당'
            
      elif type =='cello':
            # 첼로
            typeNm = '첼로폼'
      
      return send_file(r'D:\\m_project\\excelFile\\moms\\'+clsdate+'\\' + str(serialNo)+'_'+cutseq+'_'+outKinds+typeNm+'.xlsx', as_attachment=True)

@main.route('/downExcel', methods=['POST','GET'])
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


@main.route('/downTxt/<cDate>', methods=['POST','GET'])
def downTxt(cDate):
      
      db_class = dbModule.Database()
      sql = "SELECT A.ORD_OPT_NO,B.invoice_no FROM moms_request_data A INNER JOIN (SELECT MAX(ORD_OPT_NO) AS ORD_OPT_NO,invoice_no FROM cello_request_data WHERE trs_type <> '명품당일배송' GROUP BY  ORD_OPT_NO) B ON  A.ORD_OPT_NO =B.ORD_OPT_NO"
      reVal = db_class.executeAll(sql)   
      date = db_class.executeOne("select max(ins_date) ins_date from cello_request_data")[0]
      output = ''
      if len(reVal)!=0:
            for row in reVal:
                  output += row[0]+'\t'+row[1]+'\n'
            
            buffer = StringIO()
            buffer.write(output)
            response = make_response(buffer.getvalue())
            response.headers['Content-Disposition'] = 'attachment; filename='+str(date)+'_CJ_OUT_RESULT.txt'
            response.mimetype = 'text/csv'
            return response
      else:
            flash("생성 된 데이터가 없습니다.")
            return redirect(url_for('excel.excelDownload',pDate=cDate))    


@main.route('/downTxt2/<cDate>', methods=['POST','GET'])
def downTxt2(cDate):
      
      db_class = dbModule.Database()
      sql = "SELECT A.ORD_OPT_NO,B.invoice_no FROM moms_request_data A INNER JOIN (SELECT MAX(ORD_OPT_NO) AS ORD_OPT_NO,invoice_no FROM cello_request_data where trs_type ='명품당일배송' GROUP BY  ORD_OPT_NO) B ON  A.ORD_OPT_NO =B.ORD_OPT_NO"
      reVal = db_class.executeAll(sql)   
      date = db_class.executeOne("select max(ins_date) ins_date from cello_request_data")[0]

      output = ''
      
      if len(reVal)!=0:
            for row in reVal:
                  output += row[0]+'\t'+row[1]+'\n'
            
            buffer = StringIO()
            buffer.write(output)
            response = make_response(buffer.getvalue())
            response.headers['Content-Disposition'] = 'attachment; filename='+str(date)+'_TEAM_FRESH_OUT_RESULT.txt'
            response.mimetype = 'text/csv'
            return response
      else:
            flash("생성 된 데이터가 없습니다.")
            return redirect(url_for('excel.excelDownload',pDate=cDate))    


@main.route('/downingTxt/<cDate>', methods=['POST','GET'])
def downingTxt(cDate):
      
      db_class = dbModule.Database()
      sql = "SELECT CUT_OFF_NO,ORD_NO,ORD_OPT_NO,PROC_NM,ORD_NM,TRS_NM,TRS_ZIP,TRS_ADDR,TRS_ADDR2,TRS_ADDR3,TRS_PHONE,TRS_MOBILE,GDS_COMBINE,GDS_LOCATION,GDS_OPT,ORD_QTY,GDS_TYPE,BRD_NM,GIFT,TRS_MSG,STL_NO,BARCODE,TRS_INVOICE_NO FROM (SELECT A.*,B.invoice_no FROM moms_request_data A LEFT JOIN (SELECT ORD_OPT_NO,MIN(invoice_no) AS invoice_no FROM cello_request_data GROUP BY ORD_OPT_NO) B ON A.ORD_OPT_NO =B.ORD_OPT_NO )A WHERE A.invoice_no IS NULL "
      reVal = db_class.executeAll(sql)   
      date = db_class.executeOne("select max(ins_date) ins_date from cello_request_data")[0]
      
      column=['CUT_OFF_NO','ORD_NO','ORD_OPT_NO','PROC_NM','ORD_NM','TRS_NM','TRS_ZIP','TRS_ADDR','TRS_ADDR2','TRS_ADDR3','TRS_PHONE','TRS_MOBILE','GDS_COMBINE','GDS_LOCATION','GDS_OPT','ORD_QTY','GDS_TYPE','BRD_NM','GIFT','TRS_MSG','STL_NO','BARCODE','TRS_INVOICE_NO']
      df = pd.DataFrame(list(reVal),columns=column)
      
      if len(df)!=0:
            strIO = io.BytesIO()
            excel_writer = pd.ExcelWriter(strIO,engine="xlsxwriter")
            df.to_excel(excel_writer,sheet_name='sheet1', index=None)
            
            # workbook = excel_writer.book
            # worksheet = excel_writer.sheets['sheet1']
            # for i, col in enumerate(df.columns):
            #       column_len = df[col].astype(str).str.len().max()
            #       column_len = max(column_len, len(col)) + 2
            #       worksheet.set_column(i, i, column_len)
            
            excel_writer.save()
            strIO.seek(0)
                        
            return send_file(strIO,attachment_filename=str(date)+'_미출고건.xlsx', as_attachment=True)
      else:
            flash("생성 된 데이터가 없습니다.")
            return redirect(url_for('excel.excelDownload',pDate=cDate))  

@main.route('/packing_x/<cDate>', methods=['POST','GET'])
def packing_x(cDate):
      
      db_class = dbModule.Database()
      # sql = "SELECT spr_nm,trs_type,ord_no,ord_opt_no,invoice_no,total_qty,packing_qty,qty_yn FROM cello_request_data WHERE qty_yn<>'O' and trs_type='일반배송'"
      # sql = "SELECT spr_nm,trs_type,ORD_NO,ORD_OPT_NO,MAX(invoice_no) AS invoice_no FROM cello_request_data where qty_yn ='X' AND trs_type='일반배송' GROUP BY spr_nm,trs_type,ord_no,ORD_OPT_NO"
      sql = "SELECT spr_nm,trs_type,ORD_NO,ORD_OPT_NO,invoice_no,packing_qty FROM cello_request_data where qty_yn ='X' AND trs_type='일반배송' ORDER BY ORD_NO,ORD_OPT_NO"
      reVal = db_class.executeAll(sql)   
      date = db_class.executeOne("select max(ins_date) ins_date from cello_request_data")[0]
      
      column=[' 화주명 ','   출고작업유형   ',' 오더번호 ',' 일련번호 ',' 분할송장번호 ','  박스내 패킹갯수  ']
      df = pd.DataFrame(list(reVal),columns=column)
      
      if len(df)!=0:
            strIO = io.BytesIO()
            excel_writer = pd.ExcelWriter(strIO,engine="xlsxwriter")
            df.to_excel(excel_writer,sheet_name='sheet1', index=None)
            
            workbook = excel_writer.book
            worksheet = excel_writer.sheets['sheet1']
            for i, col in enumerate(df.columns):
                  column_len = df[col].astype(str).str.len().max()
                  column_len = max(column_len, len(col)) + 2
                  worksheet.set_column(i, i, column_len)
            excel_writer.save()
            strIO.seek(0)
                        
            return send_file(strIO,attachment_filename=str(date)+'_패킹합포X.xlsx', as_attachment=True)
      else:
            flash("생성 된 데이터가 없습니다.")
            return redirect(url_for('excel.excelDownload',pDate=cDate))   

      

@main.route('/reload_all', methods=['POST','GET'])
def reload_all():
      
      # Bizest.get_bizest_data()
      # Bizest.update_count_bizest()
      # Moms.update_count_moms()
      # Cello.upload_cello_data()
      # Cello.update_count_cello()
      
      return redirect(url_for('main.index'))
      