import tisgrabber as IC
import cv2
import numpy as np

def capture(Camera, ExposureTime=0, GainValue=0, average=1, HDR=False):		
	def average_shot(Obj, ave):
		width, height, bits, cformat = Camera.GetImageDescription()
		img_ave = np.zeros((height, width, 3))
		for i in range(ave):
			Obj.SnapImage()
			img_ave += Obj.GetImage()/ave
		img_flip = cv2.flip(img_ave, 0)
		return np.clip(img_flip, 0, 255).astype(np.uint8)
	
	def set_properties(Obj, ExposureTime, GainValue):		
		if ExposureTime==0:
			Obj.SetPropertySwitch("Exposure", "Auto", 1)
		else:
			Obj.SetPropertySwitch("Exposure", "Auto", 0)
			Obj.SetPropertyAbsoluteValue("Exposure","Value", ExposureTime)
		
		if GainValue==0:
			Obj.SetPropertySwitch("Gain", "Auto", 1)
		else:
			Obj.SetPropertySwitch("Gain", "Auto", 0)
			Obj.SetPropertyValue("Gain","Value", GainValue)

	set_properties(Camera, ExposureTime, GainValue)
	if HDR==False:
		img = average_shot(Camera, average)
		return img
	else:
		str_value=[0]
		Camera.GetPropertyAbsoluteValue("Exposure", "Value", str_value)
		exposure_ref = str_value[0]
		gain_ref = Camera.GetPropertyValue("Gain",  "Value")
		
		N = 3
		exposure_table = np.array([exposure_ref*0.5, exposure_ref, exposure_ref*2.0], dtype=np.float32)
		img_list = []
		for i in range(N):
			set_properties(Camera, exposure_table[i], gain_ref)
			img = average_shot(Camera, average)
			img_list.append(img)
		
		merge = cv2.createMergeDebevec()
		hdr = merge.process(img_list, times=exposure_table.copy())
		return hdr


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
wb_auto = 0
Camera.SetPropertySwitch("WhiteBalance", "Auto", wb_auto)
if wb_auto==0:	
	Camera.SetPropertyValue("WhiteBalance","White Balance Red", 72)
	Camera.SetPropertyValue("WhiteBalance","White Balance Green", 64)
	Camera.SetPropertyValue("WhiteBalance","White Balance Blue", 112)

#Capture Start
Camera.StartLive(1)
while True:
	#HDR capture
	hdr = capture(Camera, ExposureTime=0.0333, GainValue=16, average=2, HDR=True)
	tonemap = cv2.createTonemapDurand(gamma=2.2)
	res = tonemap.process(hdr.copy())
	res_8bit = np.clip(res*255, 0, 255).astype(np.uint8)
	img_hdr = res_8bit

	#LDR capture
	img_ldr = capture(Camera, ExposureTime=0.0333, GainValue=16, average=1, HDR=False)

	cv2.imshow("ldr", img_ldr)
	cv2.imshow("hdr", img_hdr)
	key = cv2.waitKey(10)
	if key == ord("q"):
		break
   
Camera.StopLive()    
cv2.destroyAllWindows()
