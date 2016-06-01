'''
Copyright (C) 2016, Blackboard Inc.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of Blackboard Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY BLACKBOARD INC ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BLACKBOARD INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Created on May 25, 2016

@author: shurrey
'''

from auth import AuthToken
from sessions import Sessions
from recordings import Recordings
from contexts import Contexts
from users import Users


import sys
import getopt

def main(argv):
    URL = "https://xx-csa.bbcollab.com"
    
    COMMAND = ''
    ALL = False
    AUTH = False
    SESSION = False
    RECORDING = False
    CONTEXT = False
    USER = False
    CLEANUP = False

    usageStr = "\nCollabRestDemo.py -t|--target <target root URL> -c|--command <command>\n"
    usageStr += "e.g CollabRestDemo.py -t www.collabserver.com -c authorize."

    if len(sys.argv) > 1: #there are command line arguments
        try:
            opts, args = getopt.getopt(argv,"ht:c:",["target=","command="])
        except getopt.GetoptError:
            print (usageStr)
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print (usageStr)
                sys.exit()
            elif opt == '-d':
                print ("Deleting at end of run.")
                CLEANUP = True
            elif opt in ("-t", "--target"):
                URL = arg.lstrip()
            elif opt in ("-c", "--command"):
                COMMAND = arg
            else:
                COMMAND = "Run All"
        print ('[main] Target is:', URL)
        print ('[main] Command is:', COMMAND)


    else:
        print(usageStr)
        sys.exit(2)


    #Set up some booleans for processing flags and order of processing
    if "context" in COMMAND:
        print("[main] Run context command")
        CONTEXT = True
    elif "user" in COMMAND:
        print("[main] Run user command")
        USER = True
    elif "recording" in COMMAND:
        print("[main] Run recording command")
        RECORDING = True
    elif "session" in COMMAND:
        print("[main] Run session command")
        SESSION = True
    elif "authorize" in COMMAND:
        print("[main] Run authorization command")
        AUTH = True
    else:
        print("[main] Empty Command: Run All\n")
        ALL = True


    print ('\n[main] Acquiring auth token...\n')
    authorized_session = AuthToken(URL)
    authorized_session.setToken()
    print ('\n[main] Returned token: ' + authorized_session.getToken() + '\n')
    
    if not AUTH:
        #run commands in required order if running ALL
        if USER or ALL:
            user_object = Users(URL, authorized_session.getToken())
            #process user command
            print("\n[main] Run user command: " + ('ALL' if ALL else COMMAND) + '...')
            
            user_object.getUsers(authorized_session.getToken())
            user_object.createUser(authorized_session.getToken())
            user_object.patchUser(authorized_session.getToken())
            user_object.putUser(authorized_session.getToken())
            user_object.getUser(authorized_session.getToken())
            
        if SESSION or ALL:
            #process Sessions command
            print("\n[main] Run sessions command: " + ('ALL' if ALL else COMMAND) + '...')
            session_object = Sessions(URL, authorized_session.getToken())
            
            session_object.getSessions(authorized_session.getToken())
            session_object.createSession(authorized_session.getToken())
            session_object.patchSession(authorized_session.getToken())
            session_object.putSession(authorized_session.getToken())
            session_object.getSession(authorized_session.getToken())
            session_object.getInstances(authorized_session.getToken())
            session_object.enrollModerator(user_object.getUserId(),authorized_session.getToken())
            session_object.readModeratorUrl(authorized_session.getToken())
                
        if RECORDING or ALL:
            #process Recordings command
            print("\n[main] Run recording_object command: " + ('ALL' if ALL else COMMAND) + '...')
            recording_object = Recordings(URL, authorized_session.getToken())
            
            recording_object.getRecordings(authorized_session.getToken())

        if CONTEXT or ALL:
            #process course command
            print("\n[main] Run Context command: " + ('ALL' if ALL else COMMAND) + '...')
            context_object = Contexts(URL, authorized_session.getToken())
                            
            context_object.getContexts(authorized_session.getToken())

    #clean up if not using individual commands
    if ALL:
        print('\n[main] Completing Demo and deleting created objects...')
        #print ("[main] Deleting Session")
        session_object.deleteSession(authorized_session.getToken())
        print ("[main] Deleting User")
        user_object.deleteUser(authorized_session.getToken())
    else:
        print("\nRemember to delete created demo objects!")


    print("[main] Processing Complete")


    
    
    
if __name__ == '__main__':
    main(sys.argv[1:])