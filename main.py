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
        self.sub_name = "hackathon2016TopCam"
        self.clean_subscribers(self.sub_name)        
        
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
        img_array = self.videoDevice.getImageRemote(self.sub_name)
        width = img_array[0]
        height = img_array[1]
        
        frame=np.asarray(bytearray(img_array[6]), dtype=np.uint8)
        frame=frame.reshape((height,width,3))
        frame = frame[height/5:height-height/5,width/4:width-width/4] 
        im = Image.fromarray(frame)
        im.save(path)
                    
    def recognizeObject(self):
        print "getting image"
        self.getAndSaveImage(self.img_name)
        
        # classify image
        print "getting classification"
        res = classifier.run_inference_on_image(self.img_name)[0]
        print res
        
        if type(res) == dict:
            #get label with highest probabilty 
            label = res["label_name"].split(",")[0]
            prob = str(int(res["score"]*100))
            return [label,prob]            
        else:
            print "result type is not a dict"
            return None
 
class HeadController():
    def __init__(self,ip,port):
        self.motion = ALProxy("ALMotion",ip,port)
        self.motion.setStiffnesses("Head",1.0)
        # contains 5 hard coded head yaw and pitch angles
        self.angles = [[-0.829349559873, -0.0117052046163],[-0.334127543218, 0.0594786450711],[-0.003150604247 , 0.047208706762],[0.0499896272058 ,0.437312890742],[ 0.524700755346 , 0.0525692697978]]
        self.num_objects = 5
        self.cur_object = 0

    def moveHeadToNextObject(self):
        self.motion.setAngles("Head",self.angles[self.cur_object],0.1)
        self.cur_object = (self.cur_object+1)%self.num_objects
        time.sleep(2) # give the robot some time to stabilize, that the image is not blurry

class Controller:
    def __init__(self,ip,port):
        img_name = "image.jpg"
        self.im = ImageManager(ip,port,img_name)
        self.im.subscribe()
        self.hc = HeadController(ip,port)
        self.tts = ALProxy("ALTextToSpeech",ip,port)
        self.sm = SubscriptionMaster(ip,port)
        self.do_stuff = False
        self.sm.subscribe("FrontTactilTouched",self.touched)
        self.tts.say("Touch me on my front sensor to recognize an object")

    def touched(self,value):
        self.do_stuff = True
        
    def startReco(self):
        self.tts.post.say("Ok, let's see.")
        self.hc.moveHeadToNextObject()
        res = self.im.recognizeObject()
        if res is None:
            self.tts.say("No object could be recognized")
        else:
            self.tts.say("I have recognized a "+res[0]+" with a probability of" + res[1] + " percent")
            
if __name__ == "__main__":
    c = Controller(IP,PORT)
    while True:
        if c.do_stuff:
            c.startReco()
            c.do_stuff = False
        else:
            time.sleep(0.1)
    c.im.unsubscribe()
    
    