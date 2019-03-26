import cv2  
import imutils
from imutils import perspective 
from imutils.video import count_frames
import numpy as np
from matplotlib import pyplot as plt 
import time
from ferramentas import image_utils
from svm import SVM


path = 'videos/p2.mp4'
vs = cv2.VideoCapture(path)
fps = 12
capSize = (640,360)
#capSize = (1920,1080)
#fourcc = cv2.VideoWriter_fourcc(*'DIVX')
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter()
success = out.open('./teste5.mp4',fourcc,fps,capSize,True)

num_frames = count_frames(path)
print(num_frames)


get_point = False  #In this version always False, will be updated soon
i = 0 

while i < num_frames:
    ret, frame = vs.read()

    frame = imutils.resize(frame, width=800)  

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("gray ", gray )

    gau = cv2.GaussianBlur(gray, (7, 7), 0)
    #cv2.imshow("gau ", gau )

    vertical = np.hstack((gray,gau))
    #cv2.imshow("vertical ", vertical )
    

    # Not work yet

    if get_point == True:
        number_of_places = 2 # Defini o numero de vagas que você irá selecionar 
        boxes = image_utils.getSpotsCoordiantesFromImage(frame, number_of_places)
        boxes = asarray(boxes)
        print(boxes)
        check = False

    else:
        #box1 = np.array([(130.14516129032256, 226.74999999999994), (85.68951612903224, 223.12096774193543), (121.97983870967742, 175.0362903225806), (155.5483870967742, 179.57258064516125)])       
        #box2 = np.array ([(137.4032258064516, 225.84274193548384), (166.43548387096774, 173.22177419354836), (210.89112903225805, 177.758064516129), (196.375, 226.74999999999994)])
        
        box1 = np.array([(246.27419354838705, 401.8870967741935), (304.3387096774193, 301.8870967741935), (376.91935483870964, 311.5645161290322), (346.2741935483871, 405.11290322580635)])
        box2 = np.array ([(233.37096774193546, 401.8870967741935), (144.66129032258064, 392.20967741935476), (210.79032258064515, 311.5645161290322), (275.3064516129032, 318.016129032258)])
        boxes = [box1, box2]
    #print('afdasdf')
    #print(box1[0].shape)

    img_resize = image_utils.getRotateRect(gau, boxes)
    feature = image_utils().extract_features(img_resize)

    '''feature1 = feature.reshape(-1, 1)
    score0 = SVM().predict(feature1)
    score1 = SVM().predict(feature[1])

    print (score0, score1)'''

    score = SVM().predict(feature)

    if score[0] == 0: 
        cv2.polylines(frame,np.int32([box1]), True ,(0,0,255),2  )
    else:
        cv2.polylines(frame,np.int32([box1]),True,(0,255,0), 2)

    if score[1] == 0: 
        cv2.polylines(frame,np.int32([box2]), True ,(0,0,255),2  )
    else:
        cv2.polylines(frame,np.int32([box2]),True,(0,255,0), 2)



    

    cv2.imshow("frame", frame)

    key = cv2.waitKey(1) & 0xFF
    # Se a tecla 'q' for pressionada, finaliza com o loop
    if key == ord("q"):
        break

    if key == ord('p'):
        hist = cv2.calcHist([a[1]], [0], None, [256], [0,256])
        plt.plot(hist)
        plt.show()


    i += 1 








