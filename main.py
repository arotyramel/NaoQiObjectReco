#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from naoqi import ALProxy
import subprocess
from vision_definitions import kQQVGA,kVGA,kQVGA,k16VGA,kRGBColorSpace,kBGRColorSpace,kDepthColorSpace
import Image
import numpy as np

import classify_image as classifier
IP = "max.local"
PORT = 9559

# from subscriptionMaster import  SubscriptionMaster
# sm = SubscriptionMaster(IP,PORT)


class ImageManager():
    def __init__(self,ip,port):
        self.videoDevice = ALProxy("ALVideoDevice", ip,port)
        self.sub_name = "hackathon2016TopCam2"
        self.clean_subscribers(self.sub_name)
        
    def subscribe(self):
        self.sub_name =  self.videoDevice.subscribeCamera(self.sub_name,0,kQVGA,kRGBColorSpace,5)

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
        im = Image.fromarray(frame)
        im.save(path)
 

if __name__ == "__main__":
    im = ImageManager(IP,PORT)
    print "Subscribe"
    im.subscribe()
    img_name = "image.jpg"
    while True:
        print "getting image"
        im.getAndSaveImage(img_name)
        
        # classify image
        print "getting classification"
        res = classifier.run_inference_on_image(img_name)[0]
        print res
        
        if type(res) == dict:
            tts = ALProxy("ALTextToSpeech",IP,PORT)
            label = res["label_name"].split(",")[0]
            tts.say("I have recognized a "+label+" with a probability of" + str(int(res["score"]*100)) + " percent")
        else:
            print "result type is not a dict"
            break
    im.unsubscribe()
    
    