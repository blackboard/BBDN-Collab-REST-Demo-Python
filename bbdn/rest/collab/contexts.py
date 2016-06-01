
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

class Contexts():
    def __init__(self, target_url, token):
        self.target_url = target_url
        self.token = token
        self.CONTEXTS_PATH = '/contexts'

    def execute(self, command, token):

        if "create" in command:
            print('[Context:execute] : ' + command)
            self.createContext(token)
        elif "read_all" in command:
            print('[Context:execute] : ' + command)
            self.getContexts(token)
        elif "read" in command:
            print('[Context:execute] : ' + command)
            self.getContext(token)
        elif "update" in command:
            print('[Context:execute] : ' + command)
            self.updateContext(token)
        elif "delete" in command:
            print('[Context:execute] : ' + command)
            self.deleteContext(token)


    def getContexts(self, token):
        print('[Context:getContexts] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Context:getContexts] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert
        print("[Context:getContexts] GET Request URL: https://" + self.target_url + self.CONTEXTS_PATH)
        print("[Context:getContexts] JSON Payload: NONE REQUIRED")
        r = session.get("https://" + self.target_url + self.CONTEXTS_PATH, headers={'Authorization':authStr}, verify=False)
        print("[Context:getContexts] STATUS CODE: " + str(r.status_code) )
        print("[Context:getContexts] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")