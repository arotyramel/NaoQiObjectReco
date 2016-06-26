#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from naoqi import ALProxy
import subprocess
from vision_definitions import kQQVGA,kVGA,kQVGA,k16VGA,kRGBColorSpace,kBGRColorSpace,kDepthColorSpace
import Image
import numpy as np
from subscriptionMaster import  SubscriptionMaster
import classify_image as classifier
from __builtin__ import True
IP = "max.local"
PORT = 9559
import time


class ImageManager():
    def __init__(self,ip,port,img_name):
        self.img_name=img_name
        self.videoDevice = ALProxy("ALVideoDevice", ip,port)
        self.sub_name = "hackathon2016TopCam5"
        self.clean_subscribers(self.sub_name)
        self.tts = ALProxy("ALTextToSpeech",ip,port)
        self.sm = SubscriptionMaster(ip,port)
        self.do_stuff = False
        self.sm.subscribe("Hackathon/event1",self.classifyImageLoop)
        
        
    def subscribe(self):
        self.sub_name =  self.videoDevice.subscribeCamera(self.sub_name,1,kQVGA,kRGBColorSpace,5)

    def unsubscribe(self):
        self.videoDevice.unsubscribe(self.sub_name)
    def clean_subscribers(self,sub_name):
        for i in range(0,8):
            try :
                videoDevice.unsubscribe(sub_name + "_%d"%i)
            except :                    
                pass
            
    def getAndSaveImage(self,path):
        time.sleep(2)
        img_array = self.videoDevice.getImageRemote(self.sub_name)
        width = img_array[0]
        height = img_array[1]
        
        frame=np.asarray(bytearray(img_array[6]), dtype=np.uint8)
        frame=frame.reshape((height,width,3))
        frame = frame[height/5:height-height/5,width/4:width-width/4] 
        im = Image.fromarray(frame)
        im.save(path)
        
    def classifyImageLoop(self,value):
        if self.do_stuff is False:
            self.do_stuff = True
            
    def doStuff(self):
        print "getting image"
        im.getAndSaveImage(self.img_name)
        
        # classify image
        print "getting classification"
#         try:
        res = classifier.run_inference_on_image(self.img_name)[0]
#         except Exception as exc:
#             print "no valid result"
#             print exc
#             self.tts.say("HAHAHAHAH")
#             return
        print res
        
        if type(res) == dict:
            label = res["label_name"].split(",")[0]
            self.tts.say("I have recognized a "+label+" with a probability of" + str(int(res["score"]*100)) + " percent")
            self.sm.memory.raiseEvent("Hackathon/event2",1)
        else:
            print "result type is not a dict"
 

if __name__ == "__main__":
    img_name = "image.jpg"
    im = ImageManager(IP,PORT,img_name)
    print "Subscribe"
    im.subscribe()
    while True:
        if im.do_stuff:
            im.doStuff()
            im.do_stuff = False
        else:
            time.sleep(0.1)
    im.unsubscribe()
    
    