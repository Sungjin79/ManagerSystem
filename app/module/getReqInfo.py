import mysql.connector
from app.module import dbModule

 
class getSessionInfo():
    def getMomsinfo(self):
        db_class = dbModule.Database()
        sql = 'select authorization,cookie FROM moms_request_value where 1=1 '
        reVal = db_class.executeOne(sql)
        header = {
        'authorization' : reVal[0],
        'content-type' : 'application/json',
        'cookie' : reVal[1]
        }
        return header

    def getCelloinfo(self):
        db_class = dbModule.Database()
        sql = 'select ajaxUid,browserUid,cellosessionkey FROM cello_request_value where 1=1 '
        reVal = db_class.executeOne(sql)        
        header = {
        'ajaxUid' : reVal[0],
        'browserUid' :reVal[1],
        'cellosessionkey' :reVal[2],
        'content-type' : 'application/json',
        'Content-Length':'633',
        'Host':'cello.samsungscl.com'
        }
        return header
        