import tisgrabber as IC
from lib import easyCap
import cv2
import numpy as np

#Create the camera object
Camera = IC.TIS_CAM()
#Print all devices
Devices = Camera.GetDevices()
for i in range(len( Devices )):
    print( str(i) + " : " + str(Devices[i]))
#Show dialog
Camera.ShowDeviceSelectionDialog()
#No devices
if Camera.IsDevValid() != 1:
	print( "No device selected")
	exit()

#Property Setting
Camera.SetPropertySwitch("Exposure", "Auto", 0)
Camera.SetPropertyAbsoluteValue("Exposure", "Value", 0.303)

Camera.SetPropertySwitch("Gain", "Auto", 0)
Camera.SetPropertyValue("Gain", "Value", 10)

Camera.SetPropertySwitch("WhiteBalance", "Auto", 0)
Camera.SetPropertyValue("WhiteBalance","White Balance Red", 72)
Camera.SetPropertyValue("WhiteBalance","White Balance Green", 64)
Camera.SetPropertyValue("WhiteBalance","White Balance Blue", 112)

#Capture Start
Camera.StartLive(0)
while True:
    Camera.SnapImage()
    img_cap = Camera.GetImage()
    img_cap = cv2.flip(img_cap, 0)

    cv2.imshow("cap", img_cap)
    key = cv2.waitKey(10)
    if key == ord("q"):
        break

Camera.StopLive()
cv2.destroyAllWindows()
