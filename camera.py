import cv2 #需要提前安装opencv


def paishe():
    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    cv2.imwrite(r"C:\Users\19022\Desktop\TaiTouLv_Jiance\TaiTouLv_Jiance\faces\classroomnow.jpg",
                img)  # 此处填写摄像头拍摄的照片的存储路径
    cv2.waitKey(0)
    # 释放摄像头资源
    cap.release()
t1="classroom"
t2="now"

if t1 == "classroom" and t2 == "now":
    paishe()



