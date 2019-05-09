import cv2
import tisgrabber as IC
from lib import easyCap

#Create the camera object
Camera = IC.TIS_CAM()
#Show dialog
Camera.ShowDeviceSelectionDialog()
#No devices
if Camera.IsDevValid() != 1:
    print( "No device selected")
    exit()

#Capture Start
while True:
    img_cap = easyCap.capture(Camera)

    cv2.imshow("cap", img_cap)
    key = cv2.waitKey(10)
    if key == ord("q"):
        break
   
cv2.destroyAllWindows()
