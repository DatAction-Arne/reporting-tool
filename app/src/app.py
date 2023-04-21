from requests.auth import HTTPBasicAuth
from requests.structures import CaseInsensitiveDict
#from natsort import natsorted, index_natsorted
from datetime import datetime
from connector import Connector
from WebServices import WebServices
import pandas as pd
import time
import requests
import json
#import plotly
#import plotly.express as px
import numpy as np
import asyncio
from aiohttp import ClientSession

url = 'https://a0010641.mobicontrol.cloud/MobiControl/api'
clientID = "0b14be23494a4a2bb1f8ea18476a13a9"
clientSecret = "ChUbPubT/kFVHYM0nHt7s3vENw/bOLvN"
username = "API"
password = "Welcome1234"
access_token = ""
refresh_token = ""

service = WebServices(url, clientID, clientSecret, username, password)
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

#deviceGroups = ['\\\\DatAction\\Demo devices\\Honeywell',  '\\\\DatAction\\Demo devices', '\\\\DatAction\\Demo devices\\Beurs Antwerp', '\\\\DatAction\\Demo devices\\Zebra',
#                '\\\\DatAction\\Demo devices\\Hubert De Backer', '\\\\DatAction\\Demo devices\\Pur Natur', '\\\\DatAction\\Demo devices\\Test Intern']

deviceGroups = ['\\\\DatAction\\Demo devices\\Test Intern', '\\\\DatAction\\Demo devices\\Honeywell', '\\\\DatAction\\Demo devices\\Zebra']

conn = Connector("localhost", "root", "AVEave2021!", "test")
conn.cursor()
conn.createTable("Mobicontrol", 
                 "url VARCHAR(255), clientID VARCHAR(100) UNIQUE, clientSecret VARCHAR(100) UNIQUE, username VARCHAR(30), password VARCHAR(30), access_token LONGTEXT, refresh_token LONGTEXT")

conn.insertTable('Mobicontrol', 
                 ['url', 'clientID', 'clientSecret', 'username', 'password', 'access_token', 'refresh_token'],
                 (url, clientID, clientSecret, username, password, access_token, refresh_token),
                 ignore=True)

print('............')

t1 = time.perf_counter()
print("1 ", t1-t1)
response = service.getData([service.url + '/devices'])

#response = asyncio.run(service.getData([service.url + '/devices']))


t2 = time.perf_counter()
print("2 ", t2-t1)
conn.updateTable("Mobicontrol", "access_token", service.token['access_token'], "clientID", service.clientID)
conn.updateTable("Mobicontrol", "refresh_token", service.token['refresh_token'], "clientID", service.clientID)
t3 = time.perf_counter()
print("3 ", t3-t1)

response = service.getData([service.url + '/devices'])
#response = asyncio.run(service.getData([service.url + '/devices']))
#print(response[0].result())

t4 = time.perf_counter()
print("4 ", t4-t1)
response_dict = dict(zip([i for i in range(0, len(response[0].result()))], response[0].result()))
#response_dict = dict(zip([i for i in range(0, len(response[0]))], response[0]))

df = pd.DataFrame(response_dict).T


columns = ['DeviceId', 'BuildVersion', 'CellularTechnology', 'AgentVersion', 'Memory', 'BatteryStatus', 'CellularCarrier', 'CellularSignalStrength', 
           'CustomData', 'HardwareSerialNumber', 'IMEI_MEID_ESN', 'IsAgentCompatible', 'IsOSSecure', 'LastCheckInTime', 'LastAgentConnectTime', 
           'LastAgentDisconnectTime',  'NetworkConnectionType', 'NetworkRSSI', 'NetworkSSID', 'OEMVersion', 'PersonalizedName', 'DeviceFirmwareUpgrade', 
           'BuildSecurityPatch', 'LifeGuardVersion', 'IsCharging', 'MXVersion', 'Kind', 'DeviceName', 'EnrollmentTime', 'Family', 'HostName',
           'IsAgentOnline', 'CustomAttributes', 'MACAddress', 'Manufacturer', 'Mode', 'Model', 'OSVersion', 'Path', 'Platform']

collectedData = ['BatteryHealthPercentage', 'BatteryChargeCycle', 'BatteryTemperature', 'ForegroundApp']

df = df.loc[:, columns]

#print(df.loc[:,'BatteryStatus'])
#print(df.loc[:,'Memory'])

df = df[df['Path'].isin(deviceGroups)]
deviceID = df['DeviceId'].values
print(deviceID)

#print(df)
t5 = time.perf_counter()
print("5 ", t5-t1)

urlList = []
for i in deviceID:
    for col in collectedData:  
        filt = '?startDate=2015-12-19T16%3A39%3A57-02%3A00&endDate=2099-04-13T16%3A39%3A57-02%3A00&builtInDataType='+col+'&order=-'
        urlList.append(service.url + '/devices/'+ i +'/collectedData'+ filt)        
        #response = service.getData(service.url + '/devices/'+deviceID[0]+'/collectedData'+filt)
        #response_dict = dict(zip([i for i in range(0, len(response.json()))], response.json()))
        #print(col, response_dict[0]['Value'])
  

t6 = time.perf_counter()
print("6 ", t6-t1)    
df = pd.DataFrame(response_dict).T

response = service.getData(urlList)
#response = asyncio.run(service.getData(urlList))

t7 = time.perf_counter()
print("7 ", t7-t1)    

#print(df.loc[:,'Path'])
#print(df)


# def formatDF(df):
#     dfInput = getDevices(df)

#     '''
#     Change format dates
#     '''
#     dfInput['Last Check-in Time'] = pd.to_datetime(dfInput['Last Check-in Time'], format='%Y-%m-%dT%H:%M:%SZ')
#     dfInput['Last Check-in Time'] =   dfInput['Last Check-in Time'].dt.strftime('%Y-%m-%d %H:%M ')

#     #dfInput['Last Security Patch Update'] = pd.to_datetime(dfInput['Last Security Patch Update'], format='%Y-%m-%d')
#     #dfInput['Last Security Patch Update'] =   dfInput['Last Security Patch Update'].dt.strftime('%d-%m-%Y')

#     return dfInput


# def loadSQL(name, df):
#     #print(df)
#     '''
#         HERE: Flatten nested DataFrame
#     '''
#     #df = pd.json_normalize(df, record_path = ['AndroidForWork'])
#     df = df.drop(columns = ['AndroidForWork', 'UserIdentities', 'Antivirus', 'Memory', 'CustomData', 'SupportedApis', 'ComplianceItems', 'CustomAttributes'])
#     #print(df)

#     db = sqlite3.connect('database.db', timeout=10, check_same_thread=False)
#     df.to_sql(name, con = db, if_exists = 'replace')
#     test = db.execute("SELECT * FROM "+name).fetchall()
#     #print(test)
#     # cursor = db.execute("SELECT * FROM "+name)
#     # names = [description[0] for description in cursor.description]


# def formatOS(df):
#     dfOS = df.OSVersion.value_counts()
#     x = natsorted(dfOS.index.values.tolist())
#     y = dfOS.loc[x].values.tolist()
#     return x, y

# def formatDate(df):
#     today = pd.to_datetime(datetime.today().strftime('%Y-%m-%d %H:%M:%S+00:00'), format='%Y-%m-%d %H:%M:%S')
#     dfDate = pd.to_datetime(df.LastCheckInTime, format='%Y-%m-%d %H:%M:%S')
#     diff = (today - dfDate).dt.days
#     for el in diff:
#         if el < 1:
#             diff = diff.replace(el, '< 1 day')
#         elif el < 2:
#             diff = diff.replace(el, '< 2 days')
#         elif el < 7:
#             diff = diff.replace(el, '< 7 days')
#         elif el < 14:
#             diff = diff.replace(el, '< 14 days')
#         elif el < 60:
#             diff = diff.replace(el, '< 60 days')
#         elif el < 90:
#             diff = diff.replace(el, '< 90 days')
#         else:
#             diff = diff.replace(el, '> 90 days')

#     x = ['< 1 day', '< 2 days', '< 7 days', '< 14 days', '< 60 days', '< 90 days', '> 90 days']
#     y = []
#     for el in x:
#         y.append(int((diff == el).sum()))
#     return x, y

# def formatManufacturer(df):
#     dfManufacturer = df.Manufacturer.value_counts()
#     x = natsorted(dfManufacturer.index.values.tolist())
#     y = dfManufacturer.loc[x].values.tolist()
#     return x, y


