import cv2
from pynput.mouse import Button, Controller
mouse = Controller()

print(cv2.__version__)
width = 1300
height = 900

class mpHands:
    import mediapipe as mp
    def __init__(self,maxHands=2,tal1=.5,tal2=.5):
        self.hands = self.mp.solutions.hands.Hands(False,maxHands,tal1,tal2)
    def Marks(self,frame):
        myHands = []
        frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            for handLandMarks in results.multi_hand_landmarks:
                myHand =[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width),int(landMark.y*height)))
                myHands.append(myHand)
        return myHands

cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

findHands = mpHands(2,.5,.5)

while True:
    ignore,  frame = cam.read()
    frame = cv2.flip(frame,1)  

    HandData = findHands.Marks(frame) 
    
    for numHand in HandData:
        mouse.position = numHand[8]
        for handlandmarks in numHand:
            cv2.circle(frame,handlandmarks,5,(255,0,0),2)
            

    #cv2.imshow('my WEBcam', frame)
    #cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break
cam.release()