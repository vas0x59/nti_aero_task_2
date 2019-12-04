import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math 
import time



rospy.init_node("Hello2")

n_in  = int(raw_input("Count: "))
m_in = float(raw_input("width: "))

x_g = 0
y_g = 0
th_g = 0

start_x = 0
start_y = 0
start_th = 0

first = True
def callback(msg):
    global first, start_th, start_x, start_y, x_g, y_g, th_g
    if first:
        start_x = msg.x*100
        start_y = msg.y*100
        start_th = msg.theta
        first = False
        # print("start  x", start_x, "y", start_y, "th", start_th)
    else:
        x_g = msg.x*100 - start_x
        y_g = msg.y*100 - start_y
        th_g = msg.theta - start_th
        if th_g < 0:
            th_g = 2 * math.pi - abs(th_g)
        # print("x", x_g, "y",  y_g, "th", th_g)


pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=20)
rospy.Subscriber("turtle1/pose", Pose, callback)

def set_vel(v, a):
    global pub
    msg = Twist()
    msg.angular.x = a[0]
    msg.angular.y = a[1]
    msg.angular.z = a[2]

    msg.linear.x = v[0]
    msg.linear.y = v[1]
    msg.linear.z = v[2]
    # msg. = v
    pub.publish(msg)

def set_a(v, a, tol):
    # set_vel(0, v)
    global th_g
    r = False
    if a < th_g:
        r = True
    while a >= th_g and not rospy.is_shutdown():
        time.sleep(0.01)
        if r:
            set_vel((0, 0, 0), (0, 0, -v))
        else:
            set_vel((0, 0, 0), (0, 0, v))
        pass
    set_vel((0, 0, 0), (0, 0, 0))
def convert(a):
    if a < 0:
        return math.pi - a
    else:
        return a
def go_to_v(v, x, y, tol, ang):
    global th_g, y_g, x_g
    # print("xy", x, y)
    set_vel((v, 0, 0), (0, 0, 0))
    while  (((x-x_g)**2 + (y-y_g) **2)**0.5) >= tol and not rospy.is_shutdown():
        # print("dist", ((x-x_g)**2 + (y-y_g) **2)**0.5) # (abs(y_g - y) > tol or abs(x_g - x) > tol) # (((x-x_g)**2 + (y-y_g) **2)**0.5) >= tol
        # print("c", x_g, y_g, "t", x, y) 
        p = (ang - th_g)
        pp = p*22
        # print("a", ang, th_g, p, pp)
        set_vel((v, 0, 0), (0, 0, pp))
        time.sleep(0.01)
    set_vel((0, 0, 0), (0, 0, 0))

a_rot = math.pi - math.radians((180.0 * (n_in - 2.0)) / n_in)
# print("a_rot", a_rot, "rad")
# while not rospy.is_shutdown():
#     # set_vel((0, 0, 0), (0, 0, 0.2))
x_prev = 0
y_prev = 0
for i in range(0, n_in):
    print(i)
    set_a(0.5, round(a_rot*(i), 10), 0.01)
    x_go = round(math.cos(a_rot*float(i)) * m_in*100 + x_g, 8)
    y_go = round(math.sin(a_rot*float(i)) * m_in*100 + y_g, 8)

    x_prev = round(math.cos(a_rot*float(i)) * m_in*100 + x_prev, 8)
    y_prev = round(math.sin(a_rot*float(i)) * m_in*100 + y_prev, 8)

    go_to_v(0.5, x_go, y_go, 0.009*100, round(a_rot*(i), 10))
    if i+1 == n_in:
        x_prev = 0
        y_prev = 0
    # print("go2", round(x_go/100, 2), round(y_go/100, 2))
    print("go", round(x_prev/100, 3), round(y_prev/100, 3))
    # print(round(math.cos(a_rot*i) * m_in + x_g, 2), round(math.sin(a_rot*i) * m_in + y_g, 2))
    # set_vel((0.5, 0, 0), (0, 0, 0))
    # time.sleep(4)

# time.sleep(0.2)
# for i in range(n_in):



# rospy.spin()