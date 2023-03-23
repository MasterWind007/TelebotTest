import cv2

class neiroFind:
    def __init__(self,  weightFile = 'nero/faces.xml'):
        self.cascade = cv2.CascadeClassifier(weightFile)
        self.sFactor = 3
        self.minNeig = 10
        

    def findFace(self,frame):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        results = self.cascade.detectMultiScale(img, scaleFactor=self.sFactor, minNeighbors=self.minNeig)
        for (x, y, w, h) in results:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
        return  frame    
             
    def setScaleFactor(self, sf):
        self.sFactor = sf

    def setMinNeighbor(self, mn):
        self.minNeig
    
    def setWeightFile(self, wf):
        self.cascade = cv2.CascadeClassifier(wf)

