from datetime import datetime
from tkinter import filedialog, simpledialog
from deepface import DeepFace
import tkinter as tk
import cv2
from tkinter import messagebox
import customtkinter
from customtkinter import CTk
import os
import PIL
from PIL import ImageTk, Image
import time

userDirPath=""
def userDirPathSet(): #set the defualt dir for the user
    global userDirPath,label
    userDirPath=filedialog.askdirectory()
    label.configure(text="Users Folder =\n"+userDirPath)

def openFile(): #to pick up a file and return it's path
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()
    return file_path

def saveProfile(name,img):
    global userDirPath
    cv2.imwrite(filename=userDirPath+"\\"+name+".jpg",img=img)

def capture_image():
    cap = cv2.VideoCapture(0)  # 0 indicates the first webcam
    ret, image = cap.read()
    if ret:
        cap.release()
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') #pre trained face detect on openCV
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)) #check if there is a face
        if len(faces) > 0:
            return 1,image
        else:
            messagebox.showerror("ERROR","No face get detected !")
            return -1,None
        
    else:
        messagebox.showerror("ERROR","Please Open the webcam ")
        return -1,None

def compare(img1,img2):   
    auth=(DeepFace.verify(img1,img2))
    print(auth) 
    word=auth['verified']
    if word==True:
        return 1
    else:
        return -1

def emotions_detect(img):
    face_analysis= DeepFace.analyze(img)
    print(face_analysis)
    print("======================================================================================")
    result=face_analysis[0]["dominant_emotion"]
    return result

#path1 = openFile()
#path2=openFile()
#img1= cv2.imread(path1)
#img2=cv2.imread(path2)
#cv2.imshow("img1",img1)
#compare(img1,img2)
#cv2.imshow("img2",img2)
#print ("RESULT: "+emotions_detect(img1))
#print ("RESULT: "+emotions_detect(img2))
#cv2.waitKey(0)
#cv2.destroyAllWindows()


#GUI CODE -----------------------------------------------------------------------------------------------------------------------------------
def cv2_to_imageTK(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
    imagePIL = PIL.Image.fromarray(image)
    imgtk = ImageTk.PhotoImage(image = imagePIL)
    return imgtk

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

APP = customtkinter.CTk()

APP.title("Happiness logger")
APP.geometry("800x750")

def select_profile(folder_path): #get the name of files on that folder
    files = []
    for file in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file)):
            temp=folder_path+"/"+file
            files.append(temp)
    return files

def page2(profile_name,shortName):
    shortName=shortName[:-4] #to remove .jpg
    frame2=customtkinter.CTkFrame(master=APP,width=800,height=750)
    frame2.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
    def call_Capture():
        def call_compare():
            #frame3=customtkinter.CTkFrame(master=APP,width=800,height=750)
            #frame3.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
            #labelWait=customtkinter.CTkLabel(master=frame3,text="Please Wait ...",font=("",50))
            #labelWait.place(relx=0.5,rely=0.5,anchor=customtkinter.CENTER)
            profileImg=cv2.imread(profile_name)
            try:
                result=compare(profileImg,img)
                if(result==1):
                    emote=emotions_detect(img)
                    file=open("report.txt", "a")
                    date = datetime.now()
                    dateString=str(date)
                    dateString=dateString[:-7]
                    resultAsString="Name: "+shortName+" Time: "+dateString+" Mood: "+ emote
                    file.write(resultAsString + "\n")  # Append text with a newline character
                    messagebox.showinfo("INFO",shortName+" HAVE BEEN LOGGED IN Succsfuly !!")
                    file.close()
                    #frame3.destroy()
                    frame2.destroy()
                else:
                    messagebox.showerror("NOT THE SAME PERSON !","Couldn't verify Please take another photo")
                    #frame3.destroy()
            except Exception as s:
                print(s)
                messagebox.showerror("ERROR","PLEASE CLEAN YOUR webcam")

        check,img=capture_image()
        if(check ==1):
            tkinterimg= cv2_to_imageTK(img)
            label= customtkinter.CTkLabel(master=frame2,text="",image=tkinterimg)
            label.place(relx=0.5,rely=0.4,anchor=customtkinter.CENTER)
            button2 = customtkinter.CTkButton(master=frame2, text="Confirm Login",
                                     width=100, height=100, font=("", 30),command=call_compare)
            button2.place(relx=0.75, rely=0.8, anchor=customtkinter.CENTER)

    button = customtkinter.CTkButton(master=frame2, text="Take a Photo",
                                     width=100, height=100, font=("", 30),command=call_Capture)
    button.place(relx=0.25, rely=0.8, anchor=customtkinter.CENTER)

def login():
    global userDirPath
    if userDirPath=="":
        messagebox.showerror("ERROR","PLEASE Enter Users Folder Path First")
        return ""
    onPath=0 #set to 0 by defualt
    #onPath is a varable that used to check of the file is on the users folder or not
    profiles=select_profile(userDirPath) #call a method that return array of users
    root = tk.Tk()
    root.withdraw()
    choosenProfile = filedialog.askopenfilename() #pick a profile from the folder
    print("Before: "+choosenProfile)
    filename = userDirPath+"/"+os.path.basename(choosenProfile) #append the path to the file to compare the profiles
    for profile in profiles:
        if(filename==profile): #if the profile get found on the dir then change onPath = 1
            onPath=1
    if(onPath==0):
        messagebox.showerror("ERROR","Please select a valid user from the Users folder")
        login()
    else:
        print("After: "+choosenProfile)
        page2(profile_name=filename,shortName=os.path.basename(choosenProfile))

def newProfile():
    global userDirPath
    if userDirPath=="":
        messagebox.showerror("ERROR","PLEASE Enter Users Folder Path First")
        return ""
    frame=customtkinter.CTkFrame(master=APP,width=800,height=750)
    frame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
    def call_Capture():

        def call_Save():
            name=simpledialog.askstring(title="Enter the name of the profile",prompt="please enter the name of the profile")
            saveProfile(name,img)
            frame.destroy()
            messagebox.showinfo("INFO","NEW PROFILE NAMED: "+name+ " HAS BEEN CREATED !")
        check,img=capture_image()

        if(check ==1):
            tkinterimg= cv2_to_imageTK(img)
            label= customtkinter.CTkLabel(master=frame,text="",image=tkinterimg)
            label.place(relx=0.5,rely=0.4,anchor=customtkinter.CENTER)
            button2 = customtkinter.CTkButton(master=frame, text="Save",
                                     width=100, height=100, font=("", 30),command=call_Save)
            button2.place(relx=0.75, rely=0.8, anchor=customtkinter.CENTER)

    button = customtkinter.CTkButton(master=frame, text="Take a Photo",
                                     width=100, height=100, font=("", 30),command=call_Capture)
    button.place(relx=0.25, rely=0.8, anchor=customtkinter.CENTER)


button = customtkinter.CTkButton(master=APP, text="Choose a Profile",
                                     width=100, height=100, font=("", 30),command=login)
button.place(relx=0.25, rely=0.8, anchor=customtkinter.CENTER)

button = customtkinter.CTkButton(master=APP, text="create a\n new profile",
                                    width=100, height=100, font=("", 30),command=newProfile)
button.place(relx=0.75, rely=0.8, anchor=customtkinter.CENTER)

button = customtkinter.CTkButton(master=APP,text="Set the users Dir"
                                    ,width=50,height=50,font=("",15),command=userDirPathSet)
button.place(relx=0.15,rely=0.1, anchor=customtkinter.CENTER)
label=customtkinter.CTkLabel(APP,text="No Users Folder Has been Selected !!!",font=("",20),text_color="red")
label.place(relx=0.5,rely=0.5,anchor=customtkinter.CENTER)



APP.mainloop()
