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
#Camera.SetPropertySwitch("Exposure", "Auto", exposure_auto)
#Camera.SetPropertySwitch("Gain", "Auto", gain_auto)
wb_auto = 1
Camera.SetPropertySwitch("WhiteBalance", "Auto", wb_auto)
if wb_auto==0:	
	Camera.SetPropertyValue("WhiteBalance","White Balance Red", 72)
	Camera.SetPropertyValue("WhiteBalance","White Balance Green", 64)
	Camera.SetPropertyValue("WhiteBalance","White Balance Blue", 112)

#Capture Start
while True:
	img_cap = easyCap.capture(Camera)

	cv2.imshow("cap", img_cap)
	key = cv2.waitKey(10)
	if key == ord("q"):
		break
   
cv2.destroyAllWindows()
