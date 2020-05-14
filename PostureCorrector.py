import cv2
import serial
import time
from firebase import firebase
import pandas as pd

#importing the classifiers
faceCascade=cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
eyeCascade=cv2.CascadeClassifier('haarcascade_eye.xml')
# noseCascade=cv2.CascadeClassifier('Nariz.xml')
# mouthCascade=cv2.CascadeClassifier('Mouth.xml')

# function to plot the boundary
def plot_edges(image, classifier, scaleFactor, minNeighbors, color, text):
    gray_image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)
    coords=[]
    for (x, y, w, h) in features:
        cv2.rectangle(image,(x,y),(x+w, y+h),color,2)
        cv2.putText(image, text, (x,y-4),cv2.FONT_HERSHEY_SIMPLEX,0.8,color,1,cv2.LINE_AA)
        coords=[x, y, w, h]
    return coords
# function to detect the face and its features
def Detect_Face(image,faceCascade,eyeCascade):
    color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
    coords = plot_edges(image, faceCascade, 1.1, 10, color['blue'],"Face")
    # print(coords)
    eyecoords=[]
    if len(coords)==4:
         # Updating region of interest by cropping image
        # roi_img = image[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]
        # Passing roi, classifier, scaling factor, Minimum neighbours, color, label text
        eyecoords = plot_edges(image, eyeCascade, 1.1, 12, color['red'], "Eye")
        print(eyecoords,type(eyecoords))
        # coords = plot_edges(roi_img, noseCascade, 1.1, 4, color['green'], "Nose")
        # coords = plot_edges(roi_img, mouthCascade, 1.1, 20, color['white'], "Mouth")
    t=[image,eyecoords]
    return t

# def initDetectFace()

def MainFunction():
    video = cv2.VideoCapture(0)
    while True:
        ret, image = video.read() # here, image is the frame
        image = Detect_Face(image,faceCascade,eyeCascade)
        cv2.imshow("Face detection",image[0])
        # key=cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'): # press q to quit program
            video.release()
            cv2.destroyAllWindows()
            return image[1]

def askImageInformation():
    print("Sit in a standard seating position\n1 to confirm \n0.to quit\n")
    a=int(input())
    if a:
        standardCoordinates = MainFunction()
        # print("standard coordinates: ",standardCoordinates)
        print("Sit in a confortable position\n1 to confirm \n0.to quit\n")
        b=int(input())
        if b:
            comfortableCoordinates = MainFunction()
            # print("comfortableCoordinates : ",comfortableCoordinates)
            print("Now you are ready to use our product")
    # print(standardCoordinates,comfortableCoordinates)
    return [standardCoordinates[1],comfortableCoordinates[1]]


# while loop to capture video feed frame by frame
def readarduino(ser):
        did=True
        while ser.inWaiting(): # Check number of characters left in buffer
            if did and ser.inWaiting() < 490: # Select last 500 characters in buffer
                for i in range(6):
                    print(ser.readline()) # Print 6 lines in buffer
                did = False
            ser.readline()

def toFireBase(data):
    firebase1 = firebase.FirebaseApplication('https://mktrs-7ac29.firebaseio.com/', None)
    # result = firebase1.get('/',None)
    # print(result['test2'])
    # firebase = firebase.FirebaseApplication('https://mktrs-7ac29.firebaseio.com/', None)
    for i in range(len(data)):
        new_user = {i:data[i]}
        result = firebase1.post('/sensordata',new_user)
        time.sleep(1)
        print(result)

def FaceIsThere():
    ser = serial.Serial('/dev/cu.usbmodem14101', 9600)
    time.sleep(1)
  # Clear buffer line by line until ser.inWaiting goes to 0
    
    readarduino(ser)
    data =[]                       # empty list to store the data
    for i in range(50):
        b = ser.readline()         # read a byte string
        string_n = b.decode()  # decode byte string into Unicode  
        string = string_n.rstrip() # remove \n and \r
        print(string)
        data.append(string)
        # df = pd.DataFrame(data,columns=['Posture'])
        # pd.concat([df1,df],sort=False)
        # df.to_csv('data.csv')
        data.append(string)           # add to the end of data list

        time.sleep(0.1)            # wait (sleep) 0.1 seconds
    readarduino(ser)
    ser.close()
    for line in data:
        print(line)
    toFireBase(data)
# standardCoordinates=[]
# confortableCoordinates=[]
definingYaxisFacecoordinates=askImageInformation()
# for i in range(len(definingYaxisFacecoordinates)):
    # print(definingYaxisFacecoordinates[i])

#initialising webcam.

if definingYaxisFacecoordinates[0]&definingYaxisFacecoordinates[1]:
    FaceIsThere()



