mport paramiko

import datetime

import requests

import os

import xml.dom.minidom

import mysql.connector

import requests

from LibEkis import *

 

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# InsecureRequestWarning отключение

 

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

res = ''

 

mysqlconnect = connectmysql()

curs=mysqlconnect.cursor()

sql='SELECT * FROM XXX_contract1 xc WHERE xc.state_=4 '

curs.execute(sql)

row=curs.fetchone()

print ("запросиз БД ",row)

print (row)

 

while row is not None:

    mysqlconnect_1 = connectmysql()

    print (row[1])

    res = splunkresult(row[1])

    if  res is not None:

      curs1 = mysqlconnect_1.cursor()

      slq_1 = ''' UPDATE XXX_contract1 set  BEGIN_DATE = %r, END_DATE=%r, State_=%r, SITE_ID_CONTRACT_NUMBER= %r WHERE  POLICY_NO=%r''' %(res[0],res[1],2,res[3],row[1])

      print('непустая ветка')

      print(slq_1)

      curs1.execute(slq_1)

      mysqlconnect_1.commit()

 

 

    elif res is None:

        curs1 = mysqlconnect_1.cursor()

        #slq_1 = ''' UPDATE XXX_contract set Policy_ID = %r, Date_Beg = %r, State_=  %r WHERE policy_Number=%r''' % ('', '', 3, row[1])

        slq_1 = ''' UPDATE XXX_contract1 set   BEGIN_DATE = %r, END_DATE=%r, State_= %r WHERE  POLICY_NO = %r ''' % ('', '',  3, row[1])

        print('пустая ветка')

        print(slq_1)

        curs1.execute(slq_1)

        mysqlconnect_1.commit()

 

    row = curs.fetchone()

 

 

 

print('Обработка завершена')
