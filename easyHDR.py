import cv2
import numpy as np
import tisgrabber as IC
from lib import easyCap 

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

#Capture Start
while True:
    #HDR capture
    hdr = easyCap.capture(Camera, Exposure=0.0333, Gain=16, average=2, HDR=True)
    tonemap = cv2.createTonemapDurand(gamma=2.2)
    res = tonemap.process(hdr.copy())
    res_8bit = np.clip(res*255, 0, 255).astype(np.uint8)
    img_hdr = res_8bit

    #LDR capture
    img_ldr = easyCap.capture(Camera, Exposure=0.0333, Gain=16, average=1, HDR=False)

    cv2.imshow("ldr", img_ldr)
    cv2.imshow("hdr", img_hdr)
    key = cv2.waitKey(10)
    if key == ord("q"):
        break
   
cv2.destroyAllWindows()
