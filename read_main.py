dom

import time

import mysql.connector

 

 

 
import datetime

import requests

import os

import xml.dom.mini
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

   # query = '''index = "ufo" earliest_time=%s latest_time=%s "message.Action"=ProjectPolicyServiceClient.loadPolicy  message.Message=Started  [search index = "ufo" %s "message.Action"=LoadPolicy | table message.CorrelationId] | spath input=message.ext.Data output=DraftPolicyID path=ns2:PolicyEOSAGORequest.DraftPolicyRequest.DraftPolicyID | search DraftPolicyID | spath input=message.ext.Data  output=DateActionBeg path=ns2:PolicyEOSAGORequest.DraftPolicyRequest.Da

 
