import cv2
import numpy
import sys, os
from skimage import io
from PIL import Image, ImageTk
import tkinter as tk
import time
from tkinter import ttk
from tkinter import IntVar
import xlrd
from tkinter import messagebox
import dlib

##登录界面
root = tk.Tk()
root.title('欢迎进入北邮抬头率检测系统！')
root.geometry('600x420')
#增加背景图片
img = Image.open(r"C:/Users/王铭炜/Desktop/Head Rate Detection/bupt.jpg")
img2 = img.resize((600, 420), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(img2)

theLabel = tk.Label(root,
                 text="",#内容
                 justify=tk.LEFT,#对齐方式
                 image=photo,
                compound = tk.CENTER,#关键:设置为背景图片
                font=("华文行楷",20),#字体和字号
                fg = "black")#前景色
theLabel.place(x=0,y=0)

def facedetec():
    cv2.namedWindow("test")#1调用摄像头
    cap=cv2.VideoCapture(0)#2人脸识别器分类器
    classfier=cv2.CascadeClassifier(r"C:/Users/王铭炜/Desktop/Head Rate Detection/haarcascade_frontalface_default.xml")
    color=(0,255,0)
    facerec = dlib.face_recognition_model_v1(r"C:/Users/王铭炜/Desktop/Head Rate Detection/dlib_face_recognition_resnet_model_v1.dat")
    sp = dlib.shape_predictor(r"C:/Users/王铭炜/Desktop/Head Rate Detection/shape_predictor_68_face_landmarks.dat")#加载检测器
    detector = dlib.get_frontal_face_detector()
    while cap.isOpened():
        ok,frame=cap.read()
        if not ok:
            break
        #3灰度转换
        grey=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #4人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
        faceRects = classfier.detectMultiScale(grey, scaleFactor = 1.2, minNeighbors = 3, minSize = (32, 32))
        if len(faceRects) > 0:            #大于0则检测到人脸
            print("检测到人脸")
            for faceRect in faceRects:  #单独框出每一张人脸
                 x, y, w, h = faceRect  #5画图
                 cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 3)#单独框出每一张人脸
        cv2.imshow("test",frame)#窗口显示
        if cv2.waitKey(10)&0xFF==ord('a'):#输入a截取图片并检测
            cap.release()

            cv2.imwrite(r"C:/Users/王铭炜/Desktop/Head Rate Detection/faces/test.jpg", frame)#保存获取图片
            img = io.imread(r"C:/Users/王铭炜/Desktop/Head Rate Detection/faces/first.jpg")#加载检测的图片
            print("ok")
            detss = detector(img,1)# 图片人脸子描述
            if (len(detss) > 0):#大于0则检测到人脸
                print("ok1")
                for k,d in enumerate(detss):
                    shape = sp(img,d)
                face_descriptor = facerec.compute_face_descriptor(img, shape)
                v = numpy.array(face_descriptor) #本地图片子描述存进v
                print("ok2")
                img = io.imread(r"C:/Users/王铭炜/Desktop/Head Rate Detection/faces/test.jpg")
                dets = detector(img, 1)# 获取图片人脸子描述
                for k, d in enumerate(dets):
                    shape = sp(img, d)
                face_descriptor = facerec.compute_face_descriptor(img, shape)
                d_test = numpy.array(face_descriptor) #boy.jpg子描述存进d_test
                print("ok3")
                # 计算欧式距离，算出人脸之间的差距
                dist = numpy.linalg.norm(v-d_test)
                dist=(1-dist)*100
            cv2.destroyAllWindows()
            cv2.waitKey(0)

            return dist
##主窗口
def get_in():
    # GUI代码
    root.destroy()
    window = tk.Tk()  # 这是一个窗口object
    window.title('抬头率监测系统')
    window.geometry('600x400')

    def read_data():
        path = r'C:/Users/王铭炜/Desktop/Head Rate Detection/pyexcel.xls'

        # 打开文件
        data = xlrd.open_workbook(path)
        # path + '/' +file 是文件的完整路径
        # 获取表格数目
        nums = len(data.sheets())
        # for i in range(nums):
        #     # 根据sheet顺序打开sheet
        #     sheet1 = data.sheets()[i]

        # 根据sheet名称获取
        sheet1 = data.sheet_by_name('Sheet1')
        sheet2 = data.sheet_by_name('Sheet2')
        # 获取sheet（工作表）行（row）、列（col）数

        nrows = sheet1.nrows  # 行
        ncols = sheet1.ncols  # 列

        # print(nrows, ncols)

        # 获取教室名称列表
        global room_name, time_name
        room_name = sheet2.col_values(0)
        time_name = sheet2.col_values(1)
        print(room_name)
        print(time_name)
        # 获取单元格数据
        # 1.cell（单元格）获取
        cell_A1 = sheet2.cell(0, 0).value
        print(cell_A1)
        # 2.使用行列索引

        cell_A2 = sheet2.row(0)[1].value

    read_data()

    def gettime():  # 当前时间显示
        timestr = time.strftime('%Y.%m.%d %H:%M', time.localtime(time.time()))
        lb.configure(text=timestr)
        window.after(1000, gettime)

    lb = tk.Label(window, text='', font=("黑体", 20))
    lb.grid(column=0, row=0)
    gettime()

    # 选择教室标签加下拉菜单
    choose_classroom = tk.Label(window, text="选择教室", width=15, height=2, font=("黑体", 12)).grid(column=0, row=1,
                                                                                               sticky='w')
    class_room = tk.StringVar()
    class_room_chosen = ttk.Combobox(window, width=20, height=10, textvariable=class_room, state='readonly')
    class_room_chosen['values'] = room_name
    class_room_chosen.grid(column=0, row=1, sticky='e')

    # 选择课时标签加下拉菜单
    choose_time = tk.Label(window, text="选择课时", width=15, height=2, font=("黑体", 12)).grid(column=0, row=2, sticky='w')
    course_time = tk.StringVar()
    course_time_chosen = ttk.Combobox(window, width=20, height=10, textvariable=course_time, state='readonly')
    course_time_chosen['values'] = time_name
    course_time_chosen.grid(column=0, row=2, sticky='e')

    pic_tip = tk.Label(window, text="所选教室时实图像", width=16, height=2, font=("黑体", 12)).grid(column=1, row=2, sticky='s')

    img = r'C:/Users/王铭炜/Desktop/Head Rate Detection/faces/start.jpg'##初始化图片界面
    img_open = Image.open(img)
    # 显示图片的代码
    (x, y) = img_open.size  # read image size
    x_s = 200  # define standard width
    y_s = y * x_s // x  # calc height based on standard width
    img_adj = img_open.resize((x_s, y_s), Image.ANTIALIAS)
    img_png = ImageTk.PhotoImage(img_adj)

    Image2 = tk.Label(window, bg='white', bd=20, height=y_s * 0.83, width=x_s * 0.83,
                      image=img_png)  ##0.83用来消除白框
    Image2.grid(column=1, row=4, sticky='w')

    flag = IntVar()
    flag.set(0)



    def rate_cal():
        face = 0

        def inspect():  ##将人脸检测函数内嵌
            nonlocal face
            str1 = "教室"
            str2 = "课上的抬头率为："
            path = r'C:/Users/王铭炜/Desktop/Head Rate Detection/faces'
            pic_path = str(class_room_chosen.get()) + str(course_time_chosen.get()) + '.jpg'
            p = path + '/' + pic_path
            img = cv2.imread(p)
            color = (0, 255, 0)

            grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            classfier = cv2.CascadeClassifier(
                r"C:/Users/王铭炜/Desktop/Head Rate Detection/haarcascade_frontalface_alt2.xml")
            eye_cascade=cv2.CascadeClassifier(
                r"C:/Users/王铭炜/Desktop/Head Rate Detection/haarcascade_eye.xml")
            faceRects = classfier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))

            a = len(faceRects)
            face = a
            str3 = str(a)

        inspect()
        path = r'C:/Users/王铭炜/Desktop/Head Rate Detection/pyexcel.xls'
        data = xlrd.open_workbook(path)
        sheet1 = data.sheet_by_name('Sheet1')
        nrows = sheet1.nrows  # 行
        ncols = sheet1.ncols  # 列
        total = 0
        for i in range(nrows):
            if (sheet1.cell(i, 0).value == class_room_chosen.get() and sheet1.cell(i,
                                                                                   1).value == course_time_chosen.get()):
                total = sheet1.cell(i, 2).value
        print(total)
        global rate
        print(face)
        rate = face /total
        print(rate)
        str1 = "教室"
        str2 = "课上的抬头率为："
        str3 = str(rate)
        var.set(class_room_chosen.get() + str1 + course_time.get() + str2 + str3)
    def paishe():
        cap = cv2.VideoCapture(0)
        ret, img = cap.read()
        cv2.imwrite(r"C:/Users/王铭炜/Desktop/Head Rate Detection/faces/classroomnow.jpg",
                    img)  # 此处填写摄像头拍摄的照片的存储路径
        cv2.waitKey(0)
        # 释放摄像头资源
        cap.release()

    def imgdetector(img_path, face_cascade_file, eye_cascade_file, show_face=True):
        image = cv2.imread(img_path)
        face_cascade = cv2.CascadeClassifier(face_cascade_file)
        if face_cascade.empty():
            raise IOError('Unable to load the face cascade classifier xml file!')
        eye_cascade = cv2.CascadeClassifier(eye_cascade_file)
        if eye_cascade.empty():
            raise IOError('Unable to load the eye cascade classifier xml file!')

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
        # 在检测到的脸部周围画矩形框
        for (x, y, w, h) in face_rects:
            if show_face: cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 3)
            roi = gray[y:y + h, x:x + w]
            eye_rects = eye_cascade.detectMultiScale(roi)
            for (x_, y_, w_, h_) in eye_rects:
                cv2.rectangle(image, (x + x_, y + y_), (x + x_ + w_, y + y_ + h_),
                              (255, 0, 0), 2)
        return image
    def pic_re():
        if (flag.get() == 0):
            t1=class_room_chosen.get()
            t2=course_time_chosen.get()
            if t1 == "classroom" and t2 == "now":
                paishe()
            pic_path = str(t1) + str(t2) + '.jpg'
            img = os.path.join(r'C:/Users/王铭炜/Desktop/Head Rate Detection/faces', pic_path) #图片的命名需按规则来命名，具体规则可参考示例图片名称
            img_open =imgdetector(img,
                          'C:/Users/王铭炜/Desktop/Head Rate Detection/haarcascade_frontalface_alt2.xml',
                          'C:/Users/王铭炜/Desktop/Head Rate Detection/haarcascade_eye.xml',
                          True)
            img_open = cv2.cvtColor(img_open, cv2.COLOR_BGR2RGB)
            img_open = Image.fromarray(img_open)
            # 显示图片的代码
            (x, y) = img_open.size  # read image size
            global x_s
            global y_s
            x_s = 200  # define standard width
            y_s = y * x_s // x  # calc height based on standard width
            img_adj = img_open.resize((x_s, y_s), Image.ANTIALIAS)
            global img_png  ##这里一定要设置为全局变量，不然图片无法正常显示！！！！！！！！！！！
            img_png = ImageTk.PhotoImage(img_adj)
            Image2.configure(image=img_png)
        window.update_idletasks()


    var = tk.StringVar()  # tkinter中的字符串
    display = tk.Label(window, textvariable=var, font=('Arial', 12), width=38, height=10)
    display.grid(column=0, row=4, sticky='n')

    # Adding a Button
    rate_button = ttk.Button(window, text="Get_rate", command=rate_cal).grid(column=0, row=4, sticky='s')

    pic_button = ttk.Button(window, text="Updata picture", command=pic_re).grid(column=0, row=5)
    window.mainloop()

def anbao1():
    passit = code_tap.get()
    if (passit == "123456"):
        messagebox.showinfo(message="密码正确，已登录")
        get_in()
    else:
        messagebox.showerror(message="密码错误,登录失败")
        root.destroy()

def anbao2():
    if (facedetec()>=50):
        messagebox.showinfo(message="密码正确，已登录")
        get_in()
    else:
        messagebox.showerror(message="密码错误,登录失败")
        root.destroy()

name = tk.Label(root, text="请输入用户名:", width=16, height=1)
name.place(x=50, y=220)
name_tap = tk.Entry(root, width=16)
name_tap.place(x=250, y=220)

code = tk.Label(root, text="请输入密码:", width=16, height=1)
code.place(x=50, y=250)
code_tap = tk.Entry(root, width=16, show="*")  # 使用show参数将密码显示为*
code_tap.place(x=250, y=250)

get_into = tk.Button(root, text='登录', command=anbao1)
get_into.place(x=250, y=300)

get_into2= tk.Button(root, text='人脸登录', command=anbao2)
get_into2.place(x=400, y=220)
root.mainloop()



# In[ ]:





