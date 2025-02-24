#####################################################################
# Ethan Patterson
# PH211 FALL 2017	Lab#: 8
# November 19th 2017
# Program finds the fall distance a human will reach if they 
# Jumped of the Crooked River Gorge Bridge, between Bend and Madras.
# While bungee jumping
#-----------------Algorithm-----------------------------------------
# 1. During free fall (rope slack) the jumper is accelerated by gravity 
#    (and drag, if enabled).
# 
# 2. Once the rope is taut, an elastic (spring) force governed by Hooke's law 
#    acts on the jumper.
# 
# 3. The simulation integrates the equations of motion (using RK4) to determine 
#    the maximum fall distance.
#
# NOTE: Instead of assuming that all gravitational potential energy is converted 
#       to spring potential energy (mgh = 1/2 k (Δs)^2), the spring constant k is 
#       provided by the user. This eliminates the assumption of perfect energy 
#       conversion and allows for experimental or realistic cord parameters.
#####################################################################
from vpython import *
import math

#---------------- Constants and Initial Conditions ----------------
t = 0              # time in seconds
dt = 0.01          # initial time step in seconds (will be adapted)

g = 9.8            # gravitational acceleration (m/s^2)
h = 91             # initial height of the jumper (m)
rop_l = 30         # unstretched rope length (m)

c_subD = 1         # drag coefficient for a human
A = pi * ((0.2/2)**2)  # cross-sectional area (m^2)

print("Congratulations, you are about to make a risky jump.")

# Ask user whether to include drag
aws = input("Is there drag? (Enter 1 for yes and 2 for no): ")
if int(aws) == 1:
    drag_on = True
else:
    drag_on = False

# Get the mass of the jumper (in kg)
m = float(input("How heavy are you? (in kg): "))
# Gravitational force (downward); note that we use a negative sign.
g_force = -m * g

# Instead of calculating k via energy conservation, ask the user for a realistic k.
k = float(input("Enter the spring constant k (in N/m) for the bungee cord: "))

Fnet = 0  # net force (N)

#----------------- State Vectors -----------------
# We'll use the y-component only; s.y is the vertical position.
s = vector(0, h, 0)  # position in meters (initially at height h)
v = vector(0, 0, 0)  # velocity in m/s (initially zero)
a = vector(0, 0, 0)  # acceleration in m/s^2
#--------------------------------------------------

#-------------- Functions: Drag and Derivatives --------------

def drag_force(v_val):
    """
    Compute the drag force (in N) that always opposes the direction of motion.
    v_val: vertical velocity (m/s)
    """
    d = 0.5 * c_subD * A * (v_val**2) * 1.225
    if v_val < 0:
        return d    # When falling, drag acts upward (positive)
    elif v_val > 0:
        return -d   # When moving upward, drag acts downward (negative)
    else:
        return 0

def derivatives(s_val, v_val, t):
    """
    Returns the derivatives ds/dt and dv/dt for the jumper.
    s_val: current vertical position (m)
    v_val: current vertical velocity (m/s)
    t: current time (s)
    """
    # Determine spring force if rope is extended.
    # The rope becomes taut when the jumper’s position is below (h - rop_l).
    if s_val <= h - rop_l:
        # Extension of the cord is (h - rop_l) - s_val.
        Fspring = k * ((h - rop_l) - s_val)
    else:
        Fspring = 0

    # Compute drag force (if enabled)
    if drag_on:
        Fdrag = drag_force(v_val)
    else:
        Fdrag = 0

    # Net force is the sum of gravitational, drag, and spring forces.
    F_net = g_force + Fdrag + Fspring
    a_val = F_net / m
    # ds/dt = v and dv/dt = a.
    return v_val, a_val

def rk4_step(s_val, v_val, t, dt):
    """
    Advances the solution one time step dt using the 4th order Runge-Kutta method.
    Returns the updated (s_val, v_val).
    """
    k1_s, k1_v = derivatives(s_val, v_val, t)
    k2_s, k2_v = derivatives(s_val + 0.5*dt*k1_s, v_val + 0.5*dt*k1_v, t + 0.5*dt)
    k3_s, k3_v = derivatives(s_val + 0.5*dt*k2_s, v_val + 0.5*dt*k2_v, t + 0.5*dt)
    k4_s, k4_v = derivatives(s_val + dt*k3_s, v_val + dt*k3_v, t + dt)
    
    s_new = s_val + (dt/6.0)*(k1_s + 2*k2_s + 2*k3_s + k4_s)
    v_new = v_val + (dt/6.0)*(k1_v + 2*k2_v + 2*k3_v + k4_v)
    return s_new, v_new

#----------------- Graphing Setup -----------------
# Using modern VPython graphing functions.
pos_graph = graph(title='Position vs. Time', xtitle='Time (s)', ytitle='Position (m)', width=750, height=250)
pcurve = gcurve(graph=pos_graph, color=color.blue)

vel_graph = graph(title='Velocity vs. Time', xtitle='Time (s)', ytitle='Velocity (m/s)', width=750, height=250)
vcurve = gcurve(graph=vel_graph, color=color.red)

acc_graph = graph(title='Acceleration vs. Time', xtitle='Time (s)', ytitle='Acceleration (m/s^2)', width=750, height=250)
acurve = gcurve(graph=acc_graph, color=color.green)
#---------------------------------------------------

# Additional parameters for adaptive time stepping:
min_dt = 0.001  # Minimum allowed time step (s)
max_dt = 0.05   # Maximum allowed time step (s)
epsilon = 0.1   # Maximum allowed displacement per time step (m)

#---------------- Combined Simulation Loop with RK4 Integration ----------------
while True:
    # Adaptive time stepping: adjust dt so that the displacement does not exceed epsilon.
    if abs(v.y) > 0:
        dt = min(max_dt, max(min_dt, epsilon / abs(v.y)))
    else:
        dt = max_dt

    # Perform a single RK4 step.
    s_new, v_new = rk4_step(s.y, v.y, t, dt)
    s.y = s_new
    v.y = v_new

    # Update acceleration from the derivatives.
    _, a_val = derivatives(s.y, v.y, t)
    a.y = a_val

    t = t + dt

    # Update the graphs.
    pcurve.plot(pos=(t, s.y))
    vcurve.plot(pos=(t, v.y))
    acurve.plot(pos=(t, a.y))

    # Terminate the simulation when the rope is extended and the jumper’s velocity becomes upward (or zero).
    if s.y <= h - rop_l and v.y >= 0:
        break

print("The simulation complete.")
print("Your maximum distance from the river is: " + str(round(s.y, 1)) + " meters")
