import cv2
from PIL import ImageTk
import sqlite3
from matplotlib import pyplot as plt
from tkinter import filedialog
import PIL.Image, PIL.ImageTk
from tkinter import *
import mysql.connector as con
import tkinter.messagebox
from PIL import ImageTk,Image
import email1

global screen
from imageai.Detection.Custom import CustomObjectDetection, CustomVideoObjectDetection
import os

execution_path = os.getcwd()

def main_screen():   
    
    global screen3
    screen3=Tk()

    C = Canvas(screen3, bg="blue", height=140, width=320)
    filename = PhotoImage(file = "186040.gif")
    background_label = Label(screen3, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    C.pack()
    screen3.configure(background='white')
    screen3.title("DASHBOARD")
    screen3.geometry('1280x720')
    
    Label(screen3, text="FIRE DETECTION SYSTEM", bg="Grey", height=1, width=100,font=("Arial Bold", 20)).pack()
    Label(screen3, text="", bg="white").pack()
    Label(screen3, text="", bg="white").pack()
    


    Label(screen3, text="", bg="white").pack()
    b0 =  Button(screen3,text="Detect From Video",height=2,width=30,bg="black",fg="white",font=("Arial Bold", 13),command=detect_from_video)
    b0.pack()

    
    Label(screen3, text="", bg="white").pack()
    b0 =  Button(screen3,text="Detect From Image",height=2,width=30,bg="black",fg="white",font=("Arial Bold", 13),command=detect_from_image)
    b0.pack()


    

def admin_login(): 
    global screen5
    global user_id
    global passw_id
    
    screen5=Tk()
    screen5.configure(background='white')
    screen5.geometry('1280x720')
    Label(screen5, text="Admin Login", font=("Arial Bold", 25),bg="grey",width=250,height=2).pack()
    Label(screen5, text="", bg="white").pack()
    Label(screen5, text="", bg="white").pack()
    name = Label(screen5, text="User Id", height=2, bg="white",font=("Arial Bold", 11))
    name.pack()
    user_id = Entry(screen5, width=20)
    user_id.pack()

    name = Label(screen5, text="Password", height=2, bg="white",font=("Arial Bold", 11))
    name.pack()
    passw_id = Entry(screen5, width=20)
    passw_id.pack()
    
    
    Label(screen5, text="", bg="white").pack()
    Label(screen5, text="", bg="white").pack()
    login1 = Button(screen5, text="Login", height=2, width=30,command=login,bg="black",fg="white",font=("Arial Bold", 13))
    login1.pack()




def login():
    name=user_id.get()
    password=passw_id.get()
    if name=="admin" and password=="admin":
        messagebox.showinfo("Information", "Login Successfull")
        screen5.destroy()
        main_screen()
        
    else:
        messagebox.showinfo("Information", "Wrong Credentials try again")
        



def train_detection_model():
    from imageai.Detection.Custom import DetectionModelTrainer

    trainer = DetectionModelTrainer()
    trainer.setModelTypeAsYOLOv3()
    trainer.setDataDirectory(data_directory="fire-dataset")
    trainer.setTrainConfig(object_names_array=["fire"], batch_size=8, num_experiments=100,
                           train_from_pretrained_model="pretrained-yolov3.h5")
    # download 'pretrained-yolov3.h5' from the link below
    # https://github.com/OlafenwaMoses/ImageAI/releases/download/essential-v4/pretrained-yolov3.h5
    trainer.trainModel()


def detect_from_image():
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k%256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter)
            break

        # elif k%256 == 27:
        #     # ESC pressed
        #     print("Escape hit, closing...")

    cv2.imwrite('E:\\FIRE DETECTION\{}.jpg'.format(img_counter), frame)
    print("{} written!".format(img_name))

    img_counter += 1
    
   

    cam.release()

    cv2.destroyWindow("test")
    detector = CustomObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(detection_model_path=os.path.join(execution_path, "detection_model-ex-33--loss-4.97.h5"))
    detector.setJsonPath(configuration_json=os.path.join(execution_path, "detection_config.json"))
    detector.loadModel()

    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path, "0.jpg"),
                                                 output_image_path=os.path.join(execution_path, "0-detected.jpg" ),
                                                 minimum_percentage_probability=40)

    for detection in detections:
        print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])
        if (detection["percentage_probability"]):
            print("Fire Detected in image with probability ="+ str (detection["percentage_probability"]))
            print("Fire Detected in image..")
            msg="Dear Admin \n  fire detected. kindly take action. \n Fire percentages are:\n"+str(detection["percentage_probability"])+"  \n Regards \n Fire Team"
            email1.email_reporting("812ashishraut1999@gmail.com",msg)    
            
    print ("END")


def detect_from_video():
    detector = CustomVideoObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(detection_model_path=os.path.join(execution_path, "detection_model-ex-33--loss-4.97.h5"))
    detector.setJsonPath(configuration_json=os.path.join(execution_path, "detection_config.json"))
    detector.loadModel()

    detected_video_path = detector.detectObjectsFromVideo(input_file_path=os.path.join(execution_path, "1.mp4"), frames_per_second=1000, output_file_path=os.path.join(execution_path, "test2-detected"), minimum_percentage_probability=40, log_progress=True )

   


    cv2.destroyAllWindows()
admin_login()


    







