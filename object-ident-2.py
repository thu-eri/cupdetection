import cv2
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
#thres = 0.45 # Threshold to detect object

classNames = []
classFile = "/home/pi/Desktop/Object_Detection_Files/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "/home/pi/Desktop/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/home/pi/Desktop/Object_Detection_Files/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)



def getObjects(img, thres, nms, draw=True, objects=[]):
    objectDetected = False
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                objectDetected = True
            
                """
                if (draw):
                    #objectDetected = True
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                   
                    
                    #print(f"{box[0]}, {box[1]}, {box[2]}, {box[3]}, {objectDetected}") #x,y, width, height = 0,1,2,3
                    
                    if box[0] > 265:
                        print ("LED on")
                        GPIO.output(18,GPIO.HIGH)
                        time.sleep(1)
                        print ("LED off")
                        GPIO.output(18,GPIO.LOW)
                        print("right side")
                      
                """    
                    
    return img,objectInfo, objectDetected


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    #cap.set(3,640)
    #cap.set(4,480)
    #cap.set(10,70)
    

    while True:
        success, img = cap.read()
        result, objectInfo, objectDetected = getObjects(img,0.45,0.2, objects=['cup'])
        print(objectInfo)

        if (objectDetected):
            print ("LED on")
            GPIO.output(18,GPIO.HIGH)
            #time.sleep(1)
            #
        else:
            print ("LED off")
            GPIO.output(18,GPIO.LOW)
        cv2.imshow("Output",img)
        cv2.waitKey(1)
  #32 , detect 4sec, undo 7