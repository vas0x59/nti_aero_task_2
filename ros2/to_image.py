import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32
from std_msgs.msg import UInt32
import cv2 
import numpy as np 
from sensor_msgs.msg import LaserScan
import math
cv = cv2
# print("first window 1")

# cv2.namedWindow('test')
# black = np.zeros((400, 400, 3), np.uint8)
# cv2.imshow('test')
# cv2.waitKey(0)

got = False
ranges = []

coords = []

def callback(msg):
    global got, ranges
    got = True
    ranges = msg.ranges
    

def proc_ranges(rng):
    crds = [np.array([math.cos(math.radians(i) - math.pi)*j, math.sin(math.radians(i) - math.pi)*j]) for i, j in enumerate(rng) if abs(j) != float('inf')]
    return crds

def proc_coords(image, crds, mm, ss):
    
    for crd in crds:
        x = crd[0] * ((ss / 2) / mm) + ss/2
        y = crd[1] * ((ss / 2) / mm) + ss/2
        if x < image.shape[1] and y < image.shape[0] and x > 0 and y > 0:
            x = int(x)
            y = int(y)
            image[y, x] = 255
    return image


rospy.init_node("Hello2_opener")

pub = rospy.Publisher('/open', UInt32)
sub = rospy.Subscriber('/scan', LaserScan, callback)


while not got:
    pass
print(len(ranges))
print(coords)
# crds = np.array(coords)
mm = 1 #m
ss = 320
est = False
prev_s = 255
st = True
angle = 0
angle_m = 0
i_m, x_m, y_m  = 0, 0, 0
def get_sum(img, x, y, w):
    ih, iw = img.shape
    if x-w < 0:
        x = w
    if y-w <0:
        y = w
    if y+w >= ih:
        y = ih-1-w
    if x+w >= iw:
        x = iw-1-w
    return np.sum(img[y-w:y+w, x-w:x+w])
rects = []
while not est and cv2.waitKey(2) != ord('q'):
    image = np.zeros((ss, ss), np.uint8)
    coords = proc_ranges(ranges)
    image = proc_coords(image, coords, mm, ss)
    # image = cv2

    kernel = np.ones((7,7),np.uint8)
    image = cv.dilate(image, kernel)
    # image = cv2.media(image, (6, 6))
    image = cv2.medianBlur(image,5)
    _, image = cv.threshold(image,2,255,cv.THRESH_BINARY)
    
    _,contours,hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cnt = max(contours, cv2.contourArea)
    # print(cnt)
    cnt = max(contours, key=cv2.contourArea)
    # cnt = contours[0]
    out = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    # print(cv2.contourArea(cnt))
    if cv2.contourArea(cnt) > 10:

        rect = cv2.minAreaRect(cnt)
        # print(rect)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        
        cv.drawContours(out,[box],0,(0,0,255),2)
        x,y,w,h = cv.boundingRect(cnt)
        cv.rectangle(out,(x,y),(x+w,y+h),(0,255,0),2)
        # print(image.shape)
        opened = False
        if x >= 0 and y >= 0 and x+w <= ss and y+h <= ss:
            img = image[y:y+h, x:x+w].copy()
            img = cv2.resize(img, (64, 64))
            cv2.imshow("img", img)
            su = np.mean(img)
            print(su, prev_s, abs(prev_s - su))
            if abs(prev_s - su)  > 7:
                # print("open")
                
                
                opened = True
            # r1 = 
            # r2 = 
            # r3 = q
            # r4 = 
            prev_s = su
        if opened == True and not st:
            angle = 0
            if i_m != 0:
                angle  = angle_m / i_m
            # print("angle", angle)
            # rectss = np.array(rects)
            # print("m_r", rectss)
            # rectm = np.mean(rects, axis=0)
            # print("m", rectm)
            rectm = [(0, 0), (0, 0), 0]
            for r in rects:
                rectm = [(rectm[0][0] + r[0][0], rectm[0][1] + r[0][1]), (rectm[1][0] + r[1][0], rectm[1][1] + r[1][1]), rectm[2] + r[2]]
            rectm = [(rectm[0][0] / len(rects), rectm[0][1] / len(rects)),
                (rectm[1][0] / len(rects), rectm[1][1] / len(rects)), rectm[2] / len(rects)]
            rectm = tuple(rectm)
            print("m", rectm)
            angle = angle
            box = cv2.boxPoints(rectm)
            box = np.int0(box)
            x1, y1 = (box[0] + box[1]) // 2
            x2, y2 = (box[2] + box[1]) // 2
            x3, y3 = (box[2] + box[3]) // 2
            x4, y4 = (box[0] + box[3]) // 2
            cv2.circle(out, (x1, y1), 3, (255, 0, 0), 1)
            cv2.circle(out, (x2, y2), 3, (255//4*3, 0, 0), 1)
            cv2.circle(out, (x3, y3), 3, (255//4*2, 0, 0), 1)
            cv2.circle(out, (x4, y4), 3, (255//4, 0, 0), 1)
            pp = [get_sum(image, x1, y1, 30), get_sum(image, x2, y2, 30), get_sum(image, x3, y3, 30), get_sum(image, x4, y4, 30)]
            exit_p = pp.index(min(pp))
            print("exit_p", exit_p)
            # s1 = get_sum()
            cv2.imshow("coords", out)
            angle = angle*0.6 + rectm[2]*0.4
            angle = exit_p*90+angle
            print("angle", angle)
            angle+=180
            print("360", angle)
            pub.publish(int(abs(angle)))
            break
            # break
        elif opened == True:
            st = False
        if not st and not opened:
            # print(rect)
            rects.append(rect)
            if len(rects) >= 20:
                rects.pop(0)
            print(rects)
            ang = rect[2]
            # x_m += rect[0][0]
            # y_m += rect[0][1]
            angle_m += ang
            print("angle", ang)
            i_m  += 1
    cv2.imshow("coords", out)
    

cv2.waitKey(0)
# rospy.spin()