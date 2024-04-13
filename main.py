import cv2
from cvzone.HandTrackingModule import HandDetector


class Button:
    def __init__(self, pos, width, height, value):
        
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value
    
    def draw(self, img):
          
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (203, 255, 192), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
        cv2.putText(img, self.value, (self.pos[0] + 40, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)

    def CheckClick(self, x, y):
        
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (255, 255, 255), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 80), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)            
            return True
        else:
            return False
        
        


# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)   # Width
cap.set(4, 720)    # height
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Creating a Button
ButtonListValues = [["7", "8", "9", "*"],
                    ["4", "5", "6", "-"],
                    ["1", "2", "3", "+"],
                    ["0", "/", ".", "="]]
ButtonList = []
for x in range(4):
    for y in range(4):
        x_pos = x * 100 + 800
        y_pos = y * 100 + 150
        ButtonList.append(Button((x_pos, y_pos), 100, 100, ButtonListValues[y][x]))

myEquation = ""
DelayCounter = 0


while True:
    
    # Get image from webcam
    success, img = cap.read()
    img = cv2.flip(img, 1)
    
    # Detection of Hnad
    hands, img = detector.findHands(img, flipType=False)
    
    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 100), (203, 255, 192), cv2.FILLED)
    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 100), (50, 50, 50), 3)    
    
    for button in ButtonList:
        button.draw(img)
    
    # Check for Hand
    if hands:
        lmList = hands[0]["lmList"]
        length, _, img = detector.findDistance(lmList[8], lmList[12], img)
        x, y = lmList[8]
        
        if length < 50:
            for i, button in  enumerate(ButtonList):
                if button.CheckClick(x, y) and DelayCounter == 0:
                    myValue = ButtonListValues[int(i % 4)][int(i / 4)]
                    if myValue == "=":
                        myEquation = str(eval(myEquation))
                    else:
                        myEquation += myValue
                    DelayCounter = 1
    
    
    # Avoid Duplicates
    if DelayCounter != 0:
        DelayCounter += 1
        if DelayCounter > 10:
            DelayCounter = 0
    
    # Display the Equation/Result
    cv2.putText(img, myEquation, (810, 120), cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)
    
    # Display the image
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    
    if key == ord("c"):
        myEquation = ""
    
    if key & 0xFF == 27:
        break    
    