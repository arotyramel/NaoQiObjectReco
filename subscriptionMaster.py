#!/usr/bin/env python


########################################################################### 
# This software is graciously provided by GenerationRobots 
# under the Simplified BSD License on
# Copyright (c) 2015, Generation Robots.
# All rights reserved.
# www.generationrobots.com
#   
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
#  this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation 
#  and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS 
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
# THE POSSIBILITY OF SUCH DAMAGE. 
# 
# The views and conclusions contained in the software and documentation are 
# those of the authors and should not be interpreted as representing official 
# policies, either expressed or implied, of the FreeBSD Project.
#
#############################################################################


import qi
import time

class SubscriptionMaster(object):
    def __init__(self,ip,port):
        connection_url = "tcp://" + ip + ":" + str(port)
        app = qi.Application(["SubscriptionMaster", "--qi-url=" + connection_url])
        super(SubscriptionMaster, self).__init__()
        app.start()
        self.memory = app.session.service("ALMemory")
        self.callback = None
        self.subscriber = {}
        
    def subscribe(self,topic,callback):
        subscriber = self.memory.subscriber(topic)
        subscriber.signal.connect(self.__cb)
        id = subscriber.signal.connect(callback)
        print "subscribed to event",topic
        self.subscriber[id] = subscriber
        return id
    
    def __cb(self,value):
        pass
        
    def unsubscribe(self,id):
        self.subscriber[id].signal.disconnect(id)
        print "unsubscribed"
        