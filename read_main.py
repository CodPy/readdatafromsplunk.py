import datetime

import requests

import os

import xml.dom.minidom

import time

import mysql.connector

 

 

 

# функция преобразования даты в формат SPLUNK

def transform_splunk_date(dt):

    Date_splunk=str (dt.month)+'/'+str (dt.day)+'/'+str (dt.year)+':'+str (dt.hour)+':'+str (dt.minute)+':'+str (dt.second)

    return Date_splunk

 

# функция подготовки запроса к SPLUNK

def createsplunkquery (Policy_number):

    EndTime_in = datetime.datetime.now()

    delta = datetime.timedelta(days=500)

    StartTime_in = EndTime_in - delta

    StartTime = transform_splunk_date(StartTime_in)

    EndTime = transform_splunk_date(EndTime_in)

    query="""index=* earliest_time=%s latest_time=%s  [search index=*  %s message.ext.ContractId!=NULL | table "message.ext.ContractId"] "message.Action"=GetOsagoContract "message.Message"=Completed "message.Node"="ufo-be-prd-05" |  spath input=message.ext.Data output=StartDate  path=CalcRequest.StartDate | spath input=message.ext.Data output=EndDate path=CalcRequest.EndDate | spath input=message.ext.Data output=Num path=LoadPolicyToRsaResult.PolicyNumber | spath input=message.ext.Data output=Draft path=LoadPolicyToRsaResult.DraftPolicyId | table StartDate, EndDate ,Num,Draft""" %(StartTime,EndTime,Policy_number)

    print(query)

   # query = '''index = "ufo" earliest_time=%s latest_time=%s "message.Action"=ProjectPolicyServiceClient.loadPolicy  message.Message=Started  [search index = "ufo" %s "message.Action"=LoadPolicy | table message.CorrelationId] | spath input=message.ext.Data output=DraftPolicyID path=ns2:PolicyEOSAGORequest.DraftPolicyRequest.DraftPolicyID | search DraftPolicyID | spath input=message.ext.Data  output=DateActionBeg path=ns2:PolicyEOSAGORequest.DraftPolicyRequest.DateActionBeg''' %(StartTime,EndTime,PolicyNumber)

 

    return query

 

# функция запроса к Splunk получение по номеру xxx договора ID полиса и даты начала действия

def splunkresult(numpolicy):

    d=()

    q ='search ' +createsplunkquery(numpolicy)

    url ='splunk.splunk.ru'

    port = '8089'

    login = 'loginsplunk'

    password = 'Passwordsplunk'

    os.environ['NO_PROXY'] = url

    searchparams = {'search': q}

    r = requests.post('https://' + url + ':' + port + '/services/search/jobs/', auth=(login, password), data=searchparams,verify=False)

    dom = xml.dom.minidom.parseString(r.text)

 

    dom.normalize()

    node1 = dom.getElementsByTagName("sid")[0]

    sid = node1.childNodes[0].nodeValue

    searchparams = {'output_mode': 'xml'}

    resp = ''

    i = 0; m = 100000

    while resp == '' and i <= m:

     print (i)

     i = i+1

     r2 = requests.get('https://' + url + ':' + port + '/services/search/jobs/'+sid+'/results?count=30',auth=(login, password),params=searchparams,verify=False)

     resp=r2.text

 

     time.sleep(0.1)

 

    dom = xml.dom.minidom.parseString(r2.text)

    #print(r2.text)

 

    dom.normalize()

 

    item=dom.getElementsByTagName('text')

    # while i<len(item):

    #  node1 = dom.getElementsByTagName("text")[0]

    #  node2=dom.getElementsByTagName("text")[1]

    #  node3=dom.getElementsByTagName("text")[2]

    #  val =node1.childNodes[0].nodeValue

    #  val1 = node2.childNodes[0].nodeValue

    #  val2 = node3.childNodes[0].nodeValue

    #  print (val1)

    #  print(val2)

    #

    #  i = i+1

    #  d = (val,val1,val2)

    #  return d

    i=0

    item = dom.getElementsByTagName('text')

    #print (item)

    #print (len(item))

    print (len(item))

    while i < len(item):

        node1 = dom.getElementsByTagName("text")[0]

        #print (node1)

        node2 = dom.getElementsByTagName("text")[1]

        node3 = dom.getElementsByTagName("text")[2]

        node4 = dom.getElementsByTagName("text")[3]

        val = node1.childNodes[0].nodeValue

        val1 = node2.childNodes[0].nodeValue

        val2 = node3.childNodes[0].nodeValue

        val3 = node4.childNodes[0].nodeValue

        i = i + 1

        d = (val, val1, val2,val3 )

      #  print('result ',d)

        return d

 

 

#функция для подключения к MySql

def connectmysql():

try:

        conn = mysql.connector.connect(host='10.221.1.39',

                                       database='intmon',

                                       user='user',

                                       password='password')

        if conn.is_connected():

         con=conn

except:

         con='error'

return con

 
