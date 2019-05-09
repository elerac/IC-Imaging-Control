"""
    The Imaging Sourceのカメラで簡単に撮影する
    
    機能:
        Exposureの設定，Gainの設定，複数枚撮影によるノイズ低減，簡易HDR

"""
import cv2
import numpy as np

def capture(Camera, Exposure, Gain, average=1, HDR=False):
    """
    Params:
        Camera: IC.TIS_CAM()で作成したインスタンス
        Exposure: 露光時間
        Gain: ゲイン
        average: 複数枚撮影の枚数（引数で入力されない場合ワンショットになる）
        HDR: Trueにすると，露光時間を変えて複数枚撮影しDebevecの手法でHDR合成する(デフォルトではFalse)
    """
        
    def average_shot(Obj, ave):
        """複数枚撮影を行う
        """
        width, height, bits, cformat = Camera.GetImageDescription()
        img_ave = np.zeros((height, width, 3))
        for i in range(ave):
            Obj.SnapImage()
            img_ave += Obj.GetImage()/ave
        img_flip = cv2.flip(img_ave, 0)
        return np.clip(img_flip, 0, 255).astype(np.uint8)
    
    def set_properties(Obj, Exposure, Gain):
        """ExposureとGainを設定する
        """
        Obj.SetPropertySwitch("Exposure", "Auto", 0)
        Obj.SetPropertyAbsoluteValue("Exposure","Value", Exposure)
        
        Obj.SetPropertySwitch("Gain", "Auto", 0)
        Obj.SetPropertyValue("Gain","Value", Gain)
    
    Camera.StartLive(0)
    set_properties(Camera, Exposure, Gain)
    if HDR==False:
        """通常撮影モード
        """
        img = average_shot(Camera, average)
        Camera.StopLive()
        return img
    else:
        """HDR撮影モード
        """
        #デフォルトのExposureとGainを取得
        str_value=[0]
        Camera.GetPropertyAbsoluteValue("Exposure", "Value", str_value)
        exposure_ref = str_value[0]
        gain_ref = Camera.GetPropertyValue("Gain", "Value")

        #Exposureのテーブルを作成
        #exposure_table = np.array([exposure_ref*0.5, exposure_ref, exposure_ref*2.0], dtype=np.float32)
        exposure_table = np.array([exposure_ref*0.25, exposure_ref*0.5, exposure_ref, exposure_ref*2.0, exposure_ref*4.0], dtype=np.float32)
        N = len(exposure_table)
        img_list = []
        for i in range(N):
            set_properties(Camera, exposure_table[i], gain_ref)
            img = average_shot(Camera, average)
            Camera.StopLive()
            img_list.append(img)
        
        merge = cv2.createMergeDebevec()
        hdr = merge.process(img_list, times=exposure_table.copy())
        return hdr
