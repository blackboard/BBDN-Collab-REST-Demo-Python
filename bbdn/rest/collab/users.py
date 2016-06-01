
"""
Copyright (C) 2016, Blackboard Inc.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of Blackboard Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY BLACKBOARD INC ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BLACKBOARD INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Created on May 25, 2016

@author: shurrey

"""

import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import time
import jwt
import datetime
import ssl
import sys

#Tls1Adapter allows for connection to sites with non-CA/self-signed
#  certificates e.g.: Learn Dev VM
class Tls1Adapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

class Users():
    def __init__(self, target_url, token):
        self.target_url = target_url
        self.token = token
        self.USERS_PATH = '/users'
        self.user_id = '';

    def execute(self, command, token):

        if "create" in command:
            print('[User:execute] : ' + command)
            self.createUser(token)
        elif "read_all" in command:
            print('[User:execute] : ' + command)
            self.getUsers(token)
        elif "read" in command:
            print('[User:execute] : ' + command)
            self.getUser(token)
        elif "patch" in command:
            print('[User:execute] : ' + command)
            self.patchUser(token)
        elif "put" in command:
            print('[User:execute] : ' + command)
            self.putUser(token)
        elif "delete" in command:
            print('[User:execute] : ' + command)
            self.deleteUser(token)

    def getUserId(self):
        return self.user_id

    def getUsers(self, token):
        print('[User:getUsers] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[User:getUsers] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert
        print("[User:getUsers] GET Request URL: https://" + self.target_url + self.USERS_PATH)
        print("[User:getUsers] JSON Payload: NONE REQUIRED")
        r = session.get("https://" + self.target_url + self.USERS_PATH, headers={'Authorization':authStr}, verify=False)
        print("[User:getUsers] STATUS CODE: " + str(r.status_code) )
        print("[User:getUsers] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")
    
    def createUser(self, token):
        print('[User:createUser] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[User:createUser] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert
        print("[User:createUser] POST Request URL: https://" + self.target_url + self.USERS_PATH)
        self.PAYLOAD = {
            #'avatarUrl':'https://pbs.twimg.com/profile_images/735102198460256256/vYaCSp-p.jpg',
            'lastName':'DeveloperDEMO',
            'firstName' :'CollaborateAPI',
            'displayName':'Collab API Demo',
            'email':'scott.hurrey@gmail.com'
            
        }
        print("[User:createUser] JSON Payload: "  + str(self.PAYLOAD))
        
        r = session.post("https://" + self.target_url + self.USERS_PATH, headers={ 'Authorization':authStr,'Content-Type':'application/json','Accept':'application/json' }, json=self.PAYLOAD, verify=False)
        print("[User:createUser] STATUS CODE: " + str(r.status_code) )
        print("[User:createUser] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            self.user_id = res['id'];
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")
            
    def patchUser(self, token):
        print('[User:patchUser] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[User:patchUser] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert
        print("[User:patchUser] PATCH Request URL: https://" + self.target_url + self.USERS_PATH+ '/' + self.user_id)
        #self.PAYLOAD = {
            #'avatarUrl':'https://pbs.twimg.com/profile_images/735102198460256256/vYaCSp-p.jpg',
        #    'lastName':'DeveloperDEMO',
        #    'firstName' :'CollaborateAPI',
        #    'displayName':'Collab API Demo',
        #    'email':'scott.hurrey@blackboard.com'
            
        #}
        #print("[User:patchUser] JSON Payload: "  + str(self.PAYLOAD))
        
        r = session.patch("https://" + self.target_url + self.USERS_PATH + '/' + self.user_id, headers={ 'Authorization':authStr,'Content-Type':'application/json','Accept':'application/json' }, json={ 'email':'scott.hurrey@blackboard.com' }, verify=False)
        print("[User:patchUser] STATUS CODE: " + str(r.status_code) )
        print("[User:patchUser] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")
            
    def putUser(self, token):
        print('[User:putUser] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[User:putUser] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert
        print("[User:putUser] PUT Request URL: https://" + self.target_url + self.USERS_PATH+ '/' + self.user_id)
        self.PAYLOAD = {
            'avatarUrl':'https://pbs.twimg.com/profile_images/735102198460256256/vYaCSp-p.jpg',
            'lastName':'DeveloperDEMO',
            'firstName' :'CollaborateAPI',
            'displayName':'Collab API Demo',
            'email':'scott.hurrey@blackboard.com'
            
        }
        print("[User:putUser] JSON Payload: "  + str(self.PAYLOAD))
        
        r = session.put("https://" + self.target_url + self.USERS_PATH + '/' + self.user_id, headers={ 'Authorization':authStr,'Content-Type':'application/json','Accept':'application/json' }, json=self.PAYLOAD, verify=False)
        print("[User:putUser] STATUS CODE: " + str(r.status_code) )
        print("[User:putUser] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")
            
    def getUser(self, token):
        print('[User:getUser] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[User:getUser] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert
        print("[User:getUser] GET Request URL: https://" + self.target_url + self.USERS_PATH + '/' + self.user_id)
        print("[User:getUser] JSON Payload: NONE REQUIRED")
        r = session.get("https://" + self.target_url + self.USERS_PATH + '/' + self.user_id, headers={'Authorization':authStr}, verify=False)
        print("[User:getUser] STATUS CODE: " + str(r.status_code) )
        print("[User:getUser] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")
    
    def deleteUser(self, token):
        print('[User:deleteUser] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[User:deleteUser] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert
        print("[User:deleteUser] DELETE Request URL: https://" + self.target_url + self.USERS_PATH + '/' + self.user_id)
        print("[User:deleteUser] JSON Payload: NONE REQUIRED")
        r = session.delete("https://" + self.target_url + self.USERS_PATH + '/' + self.user_id, headers={'Authorization':authStr}, verify=False)
        print("[User:deleteUser] STATUS CODE: " + str(r.status_code) )
        print("[User:deleteUser] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")
    