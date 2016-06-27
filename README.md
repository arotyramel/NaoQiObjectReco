# NaoQiObjectReco

Simple example with Nao using Tensor Flow for object recognition. This is an offline object recognition using a trained neural network and the Python NaoQi SDK.


#Requirements:
Python2.7
Python NaoQi SDK (almost all versions should work fine)
Tensorflow

#Install:
Follow these installation steps to install tensor flow on your machine
[Object Reco - Tensorflow](https://www.tensorflow.org/versions/r0.9/get_started/os_setup.html#test-the-tensorflow-installation)

Run the default example to recognized the pandabear.

Afterwards copy the temporary downloaded database to your NaoQiObjectReco folder
On ubuntu:
cp -r /tmp/imagenet /YOURPATH/NaoQiObjectReco/imagenet

Verify that you have the Python and the corresponding NaoQi SDK installed. Choregraph is not required. The NaoQi version does not really matter, as only basic proxy services are used.


#Usage:
Start with Nao in a relaxed sitting position and disabled motors. Place 5 objects in front of the robot. Works best, if you have a homogenous background and distinctive 
object shapes.

Move insight the NaoQiObjectReco and launch the the python script
```
python main.py
```

This example was tested on Ubuntu 14.04 64-bit with NaoQi version 2.1.4 

#Example Video:
<a href="https://www.youtube.com/watch?v=_12YpMqTVXc" target="_blank"><img src="https://lh4.googleusercontent.com/k4WAUTxlkOSEwKQlsTALw6C-Vrn4pZ5dWC8Cx62AuqDyFJhv2i956vN6IqPAOdd1uaA-cw=w1335-h616" 
alt="Nao recognizing objects" width="240" height="180" border="10" /></a>
