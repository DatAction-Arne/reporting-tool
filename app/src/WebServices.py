from requests.auth import HTTPBasicAuth
from requests.structures import CaseInsensitiveDict
from connector import Connector
import requests
import asyncio
import itertools
from aiohttp import ClientSession
from concurrent.futures import ThreadPoolExecutor

class WebServices():
    def __init__(self, url, clientID, clientSecret, username, password):
        self.url = url
        self.clientID = clientID
        self.clientSecret = clientSecret
        self.username = username
        self.password = password
        self.token = ""
        
    def requestToken(self):
        if self.token:
            try:
                payload = "grant_type=refresh_token&refresh_token=" + self.token["refresh_token"] + "&client_id=" + self.clientID + "&client_secret=" + self.clientSecret
                headers = {"Content-Type": "application/x-www-form-urlencoded"}
                r = requests.post(self.url+"/token", headers=headers, data=payload)    
                print("Refresh") 
            except:          
                payload = "grant_type=password&username=" + self.username + "&password=" + self.password
                headers = {"Content-Type": "application/x-www-form-urlencoded"}
                r = requests.post(self.url+"/token", headers=headers, auth=(self.clientID, self.clientSecret), data=payload)  
                print("New token")     
        else:                        
            payload = "grant_type=password&username=" + self.username + "&password=" + self.password
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            r = requests.post(self.url+"/token", headers=headers, auth=(self.clientID, self.clientSecret), data=payload)
            print("New token") 
        return r
    
    #async def getData(self, url):
    def getData(self, url):
        try:
            #print('try')
            header = CaseInsensitiveDict()
            header["Authorization"] = "Bearer {}".format(self.token['access_token'])
            
            with ThreadPoolExecutor(max_workers=10) as executor:
                with requests.Session() as session:
                    r = [executor.submit(self.fetch, i, header, session) for i in url]
                    
            # async with ClientSession() as session:
            #     tasks = [self.fetch(i, header, session) for i in url]                    
            #     r = await asyncio.gather(*tasks)
                
            print("Access")   
        except:
            self.token = self.requestToken().json()
            #saveToken(token, query[0][1])
            header = CaseInsensitiveDict()
            header["Authorization"] = "Bearer {}".format(self.token['access_token'])
            
            with ThreadPoolExecutor(max_workers=50) as executor:
                with requests.Session() as session:
                    r = [executor.submit(self.fetch, i, header, session) for i in url]
                    
            # async with ClientSession() as session:
            #     tasks = [self.fetch(i, header, session) for i in url]                       
            #     r = await asyncio.gather(*tasks)
                
        return r
    
    # async def fetch(self, url, header, session):
    #     async with session.get(url, headers=header) as response:
    #         return await response.json()
    
    def fetch(self, url, header, session):
        with session.get(url, headers=header) as response:
            return response.json()
    
