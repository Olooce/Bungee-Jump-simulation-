#####################################################################
# Ethan Patterson
# PH211 FALL 2017	Lab#: 8
# November 19th 2017
# Program finds the fall distance a human will reach if they 
# Jumped of the Crooked River Gorge Bridge, between Bend and Madras.
# While bungee jumping
#-----------------Algorithm-----------------------------------------
# 1. Find the velocity reached after being in free fall for
#    the length of the rop.
# 
# 2. This velocity is used to find the kinetic energy
#    Relate kinetic energy to spring potential engergy.
# 
# 3. Use Hooke's law to find the spring force and bring that into the
#    system.
#####################################################################
from visual import *
from visual.graph import *
import math

t = 0 # time in Sec
dt = .01 # Change of time in Sec

g = 9.8 # Gravity is in meters per second^2
h = 91 # Hight is in meters
rop_l = 30 # Rope length is in meters

c_subD = 1 # Drag c of a human
A = pi * ((.2/2)**2) # Area of a human

print ("Congratulations you are about to make a risky jump.")

aws = input("Is there drag 1 for yes and 2 for no: ") # Ask user to include drag or not 
if aws == 1:
	drag_on = True
else:
	drag_on = False

m = input ("How heavy are you? in kg please: ")# Mass is in kg
g_force = m * g * -1 # Force of free fall

# Found k from the equation "mgh = (1/2)(k)(del_s)^2" 
k = round((2 * m * g * h)/(h-rop_l)**2, 1) # k is in N/m

Fnet = 0 # In Newtons

#--------------Vectors-----------------
s = vector(0,h,0) # In meters
v = vector(0,0,0) # In meter/seconds
a = vector(0,0,0) # In meter/seconds^2
#--------------------------------------

#--------------Functions---------------

# Returns Drag in Newtons
def drag_force(v):
	d = 0.5 * c_subD * A * v**2 * 1.225
	return d
#--------------------------------------

#----Graphs----------------------------
gp = gdisplay(x=0, y=0, width=750, height=250, 
      title='Position vs. time', xtitle='Time', ytitle='Positon', 
      foreground=color.black, background=color.white,   
      xmax=0, xmin=180, ymax=s.y, ymin=0)
pcurve=gcurve(color = color.blue)

gp = gdisplay(x=0, y=250, width=750, height=250, 
      title='Velocity vs. time', xtitle='Time', ytitle='Velocity', 
      foreground=color.black, background=color.white, 
      xmax=0, xmin=180, ymax=v.y, ymin=0)
vcurve=gcurve(color = color.red)

gp = gdisplay(x=0, y=500, width=750, height=250, 
      title='Acceleration vs. time', xtitle='Time', ytitle='Acceleration', 
      foreground=color.black, background=color.white, 
      xmax=0, xmin=180, ymax=a.y, ymin=0)
acurve=gcurve(color = color.green)
#--------------------------------------

# h is the starting hight rop_l is the length of the rope 
while s.y > h - rop_l:
	if drag_on == True:
		Fnet = drag_force(v.y) + g_force # In Newtons
	else:
		Fnet =  g_force # In Newtons

	a.y = Fnet/m # Newtons second law
	
	v.y = v.y + a.y * dt # Change in velocity
	s.y = s.y + v.y * dt # Change in position
	t = t + dt # Updates time
	
	#UPDATE GRAPH
	pcurve.plot(pos=(t,s.y))
	vcurve.plot(pos=(t,v.y))
	acurve.plot(pos=(t,a.y))

# h is the starting hight rop_l is the length of the rope
while s.y <= h - rop_l:
	# Using Hook's law here
	Fspring = k * ((h-rop_l) - s.y) # In Newtons
	if drag_on == True:
		Fnet = g_force + drag_force(v.y) + Fspring # In Newtons
	else:
		Fnet = g_force + Fspring # In Newtons

	a.y = Fnet/m # Newtons second law
	
	v.y = v.y + a.y * dt # Change in velocity
	s.y = s.y + v.y * dt # Change in position
	t = t + dt # Updates time
	
	#UPDATE GRAPH
	pcurve.plot(pos=(t,s.y))
	vcurve.plot(pos=(t,v.y))
	acurve.plot(pos=(t,a.y))
	
	if v.y >= 0: # When velocity is zero stop the loop
		break

print "The k value is: " + str(k)

if drag_on == True:
	print "You're max distance from the river with drag  is: " + str(round(s.y,1)) + " meters"
else:
	print "You're max distance from the river without drag  is: " + str(round(s.y,1)) + " meters"
