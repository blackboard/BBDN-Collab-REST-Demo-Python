
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
from requests.packages import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import time
import jwt
import datetime
import ssl
import sys

urllib3.disable_warnings()

#Tls1Adapter allows for connection to sites with non-CA/self-signed
#  certificates e.g.: Learn Dev VM
class Tls1Adapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

class Sessions():
    def __init__(self, target_url, token):
        self.target_url = target_url
        self.token = token
        self.SESSIONS_PATH = '/sessions'
        self.SESSION_ID = ''
        self.ENROLLMENT_ID = ''
        self.GUEST_URL = ''
        self.MODERATOR_URL = ''

    def execute(self, command, token):

        if "create" in command:
            print('[Session:execute] : ' + command)
            self.createSession(token)
        elif "read_all" in command:
            print('[Session:execute] : ' + command)
            self.getSessions(token)
        elif "read" in command:
            print('[Session:execute] : ' + command)
            self.getSession(token)
        elif "update" in command:
            print('[Session:execute] : ' + command)
            self.updateSession(token)
        elif "delete" in command:
            print('[Session:execute] : ' + command)
            self.deleteSession(token)

    def getSessionId(self):
        return self.SESSION_ID
    
    def getGuestUrl(self):
        return self.GUEST_URL
    
    def getModUrl(self):
        return self.MODERATOR_URL

    def getSessions(self, token):
        print('[Session:getSessions] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Session:getSessions] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert
        print("[Session:getSessions] GET Request URL: https://" + self.target_url + self.SESSIONS_PATH)
        print("[Session:getSessions] JSON Payload: NONE REQUIRED")
        r = session.get("https://" + self.target_url + self.SESSIONS_PATH, headers={'Authorization':authStr}, verify=False)
        print("[Session:getSessions] STATUS CODE: " + str(r.status_code) )
        print("[Session:getSessions] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")
            
    def createSession(self, token):
        print('[Session:createSession] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Session:createSession] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert
        print("[Session:createSession] POST Request URL: https://" + self.target_url + self.SESSIONS_PATH)
        self.PAYLOAD = {
            "allowInSessionInvitees": 'true',
            "guestRole": "presenter",
            "openChair": 'true',
            "sessionExitUrl": "string",
            "mustBeSupervised": 'false',
            "noEndDate": 'true',
            "description": "Collab API Demo Room",
            "canPostMessage": 'true',
            "participantCanUseTools": 'true',
            "courseRoomEnabled": 'true',
            "canAnnotateWhiteboard": 'true',
            "canDownloadRecording": 'true',
            "canShareVideo": 'true',
            "name": "Collab API Demo Room",
            "raiseHandOnEnter": 'false',
            "allowGuest": 'true',
            "showProfile": 'true',
            "canShareAudio": 'true'      
        }
        print("[Session:createSession] JSON Payload: "  + str(self.PAYLOAD))
        
        r = session.post("https://" + self.target_url + self.SESSIONS_PATH, headers={ 'Authorization':authStr,'Content-Type':'application/json','Accept':'application/json' }, json=self.PAYLOAD, verify=False)
        print("[Session:createSession] STATUS CODE: " + str(r.status_code) )
        print("[Session:createSession] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            self.SESSION_ID = res['id']
            self.GUEST_URL = res['guestUrl']
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")
            
    def patchSession(self, token):
        print('[Session:patchSession] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Session:patchSession] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert
        print("[Session:patchSession] PATCH Request URL: https://" + self.target_url + self.SESSIONS_PATH+ '/' + self.SESSION_ID)
        
        r = session.patch("https://" + self.target_url + self.SESSIONS_PATH + '/' + self.SESSION_ID, headers={ 'Authorization':authStr,'Content-Type':'application/json','Accept':'application/json' }, json={ "description": "Collab API Demo Room" }, verify=False)
        print("[Session:patchSession] STATUS CODE: " + str(r.status_code) )
        print("[Session:patchSession] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")
            
    def putSession(self, token):
        print('[Session:putSession] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Session:putSession] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert
        print("[Session:putSession] PUT Request URL: https://" + self.target_url + self.SESSIONS_PATH+ '/' + self.SESSION_ID)
        self.PAYLOAD = {
            "allowInSessionInvitees": 'true',
            "guestRole": "presenter",
            "openChair": 'true',
            "sessionExitUrl": "string",
            "mustBeSupervised": 'false',
            "noEndDate": 'true',
            "description": "Collab API Demo Room",
            "canPostMessage": 'true',
            "participantCanUseTools": 'true',
            "courseRoomEnabled": 'true',
            "canAnnotateWhiteboard": 'true',
            "canDownloadRecording": 'true',
            "canShareVideo": 'true',
            "name": "Collab API Demo Room",
            "raiseHandOnEnter": 'false',
            "allowGuest": 'true',
            "showProfile": 'true',
            "canShareAudio": 'true'      
        }
        print("[Session:putSession] JSON Payload: "  + str(self.PAYLOAD))
        
        r = session.put("https://" + self.target_url + self.SESSIONS_PATH + '/' + self.SESSION_ID, headers={ 'Authorization':authStr,'Content-Type':'application/json','Accept':'application/json' }, json=self.PAYLOAD, verify=False)
        print("[Session:putSession] STATUS CODE: " + str(r.status_code) )
        print("[Session:putSession] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")
            
    def getSession(self, token):
        print('[Session:getSession] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Session:getSession] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert
        print("[Session:getSession] GET Request URL: https://" + self.target_url + self.SESSIONS_PATH + '/' + self.SESSION_ID)
        print("[Session:getSession] JSON Payload: NONE REQUIRED")
        r = session.get("https://" + self.target_url + self.SESSIONS_PATH + '/' + self.SESSION_ID, headers={'Authorization':authStr}, verify=False)
        print("[Session:getSession] STATUS CODE: " + str(r.status_code) )
        print("[Session:getSession] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")
    
    def deleteSession(self, token):
        print('[Session:deleteSession] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Session:deleteSession] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert
        print("[Session:deleteSession] DELETE Request URL: https://" + self.target_url + self.SESSIONS_PATH + '/' + self.SESSION_ID)
        print("[Session:deleteSession] JSON Payload: NONE REQUIRED")
        r = session.delete("https://" + self.target_url + self.SESSIONS_PATH + '/' + self.SESSION_ID, headers={'Authorization':authStr}, verify=False)
        print("[Session:deleteSession] STATUS CODE: " + str(r.status_code) )
        print("[Session:deleteSession] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")
            
    def getInstances(self, token):
        print('[Session:getSession] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Session:getSession] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert
        print("[Session:getSession] GET Request URL: https://" + self.target_url + self.SESSIONS_PATH + '/' + self.SESSION_ID + "/instances")
        print("[Session:getSession] JSON Payload: NONE REQUIRED")
        r = session.get("https://" + self.target_url + self.SESSIONS_PATH + '/' + self.SESSION_ID + "/instances", headers={'Authorization':authStr}, verify=False)
        print("[Session:getSession] STATUS CODE: " + str(r.status_code) )
        print("[Session:getSession] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")
            
    def getAttendees(self, token):
        print('[Session:getSession] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Session:getSession] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert
        print("[Session:getSession] GET Request URL: https://" + self.target_url + self.SESSIONS_PATH + '/' + self.SESSION_ID + "/instances")
        print("[Session:getSession] JSON Payload: NONE REQUIRED")
        r = session.get("https://" + self.target_url + self.SESSIONS_PATH + '/' + self.SESSION_ID, headers={'Authorization':authStr}, verify=False)
        print("[Session:getSession] STATUS CODE: " + str(r.status_code) )
        print("[Session:getSession] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")
            
    def enrollModerator(self,user_id, token):
        print('[Session:enrollModerator] user_id: ' + user_id)
        print('[Session:enrollModerator] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Session:enrollModerator] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert
        print("[Session:enrollModerator] POST Request URL: https://" + self.target_url + self.SESSIONS_PATH + '/' + self.SESSION_ID + "/enrollments")
        self.PAYLOAD = {
            'launchingRole':'Moderator',
            'editingPermission':'reader',
            'userId': user_id
        }
        print("[Session:enrollModerator] JSON Payload: "  + str(self.PAYLOAD))
        r = session.post("https://" + self.target_url + self.SESSIONS_PATH + '/' + self.SESSION_ID + "/enrollments", headers={'Authorization':authStr}, json=self.PAYLOAD, verify=False)
        print("[Session:enrollModerator] STATUS CODE: " + str(r.status_code) )
        print("[Session:enrollModerator] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            self.ENROLLMENT_ID = res['id']
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")
    
    def readModeratorUrl(self,token):
        print('[Session:readModeratorUrl] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Session:readModeratorUrl] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert
        print("[Session:readModeratorUrl] GET Request URL: https://" + self.target_url + self.SESSIONS_PATH + '/' + self.SESSION_ID + "/enrollments/" + self.ENROLLMENT_ID + "/url")

        print("[Session:readModeratorUrl] JSON Payload: NONE")
        r = session.get("https://" + self.target_url + self.SESSIONS_PATH + '/' + self.SESSION_ID + "/enrollments/" + self.ENROLLMENT_ID + "/url", headers={'Authorization':authStr}, verify=False)
        print("[Session:readModeratorUrl] STATUS CODE: " + str(r.status_code) )
        print("[Session:readModeratorUrl] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            self.MODERATOR_URL = res['url']
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")