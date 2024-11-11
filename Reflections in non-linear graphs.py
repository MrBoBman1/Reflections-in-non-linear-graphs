"""
Description of the program:

This program was created to investigate the behaviour of reflections in non-linear graphs.
The program takes two equations, one for the mirror line and one for the object line.

I have defined a reflection by the process of generating a 'light beam' at every point (or many points) on the mirror line.
This light beam is simply the normal to the mirror line.
The distance between the mirror and the object along this mirror line is then calculated and subtracted from the co-ordinate of the current point on the mirror line.
This effectively flips the object over the mirror line.

The inputs are: the two equations, the bounds for calculating and displaying the two lines.


This is currently a work in progress. There are a few issues with some graphs or lines being reflected when they shouldn't.
"""


"""
V1 review:

The program currently successfuly displays all three graphs and the reflected graph is accurate.

Issues:

I have encountered an issue with how I define the light beam.
The light beam is intended to emanate from a point, 'p' on the mirror line, and continue until it hits the object line.
I have implemented this by simply solving the simultaneous eqaution of 'light beam = object'
This works as intended until the object is 'behind' the mirror, which either provides two solutions, or 1 invalid solution
This is an issue as I have not defined the light beam as having a direction, this also leads to the issue of how to define the direction
as it is not so obvious how to do so with non-linear mirrors, especially discontinuous mirror lines such as 1/x.
Another issue arises when there is no solution to the light beam which only happens in two cases:
    If the object is a straight line, and the light beam happens to be perfectly parrallel then there will be no solution
    If the function of the object is only defined over a certain range, e.g. a circle

Solutions:

For now, I will continue development assuming the mirror function is a polynomial

V2 development tracker

fixed the program for OBJECTS that are not defined for some regions of the graph (not mirrors yet)

fixing issue with objects reflecting when they should be obscured
    encountered issue with floating point errors (rounding) making the light beam think it had an extra intercept with the mirror

fixing issue were max_x value for display doesnt work
"""


#imports

import matplotlib.pyplot as plt
import numpy as np
import sympy as sym
import math

#initialising
sym.init_printing()
x,y = sym.symbols('x,y',real=True)

#input desired equations for the mirror line and the reflected object in the form y = f(x)

obj_eqution = x
mirror_equation = x**2

mirror = sym.Eq(mirror_equation,y)#sympy equation for mirror line
mirror_dx = sym.Eq(sym.diff(sym.solve(mirror,y)[0],x),y)#sympy equation for the derivative of the mirror line
obj = sym.Eq(obj_eqution,y)#sympy equation for the object line

def validate_solutions(point,solutions,x_coords,y_coords,max_x,min_x):
    #checks if the solutions are valid (not obscured by the mirror itself)
    left_x_sols = []
    right_x_sols = []
    for solution in solutions:
        if int(solution) == int(point):
            right_x_sols.append(solution)
            left_x_sols.append(solution)
        elif solution < point:
            left_x_sols.append(solution)
        elif solution > point:
            right_x_sols.append(solution)
    print(left_x_sols)
    print(right_x_sols)
    #now check if the light beam re-intercepts the mirror line first
    m_sols = sym.solve(light_beam-sym.solve(mirror,y)[0],x)#the x-intersections between the MIRROR line and the light beam
    print("m-sols")
    print(m_sols)
    left_m_sols,right_m_sols = [],[]#the lists for the mirror intercepts
    for m_sol in m_sols:#there will always be one intercept, this CANNOT be ignored as if it is not removed, floating point errors can break the code

        #sort mirror intercepts into left and right and remove the origin point



        round_point = round(point,5)
        round_m_sol = round(m_sol,5)
        print("r point")
        print(round_point)
        print("r msol")
        print(round_m_sol)
        if round_m_sol == round_point:
            print("\npassed\n")
            pass
        elif round_m_sol < round_point:
            left_m_sols.append(m_sol)
        elif round_m_sol > round_point:
            right_m_sols.append(m_sol)

    if left_x_sols:#if there are any x solutions on the left
        print("left x")
        if left_m_sols:#if there are any mirror intercepts on the left
            print(left_m_sols)
            close_m_left = max(left_m_sols)#take the closest mirror solution
            for sol in left_x_sols:#for each x solution on the left
                if sol > close_m_left:#if it is closer than the mirror solution it is a valid solution
                    min_x = check_new_minormax(min_x,sol,"min")
                    y_sol = sym.solve(obj.subs(x,sol),y)[0]#the y solution to the intercept
                    x_coords.append(2*point-sol)#adds the x ordinate of the reflected point to the list
                    y_coords.append(2*sym.solve(mirror.subs(x,point),y)[0]-y_sol)#adds the y ordinate of the reflected point to the list
                    print(sol)
        else:#if there aren't any mirror solutions on the left then all x solutions are valid for the left
            print("no left m")
            for sol in left_x_sols:#for each x solution on the left
                print(sol)
                min_x = check_new_minormax(min_x,sol,"min")
                y_sol = sym.solve(obj.subs(x,sol),y)[0]#the y solution to the intercept
                x_coords.append(2*point-sol)#adds the x ordinate of the reflected point to the list
                y_coords.append(2*sym.solve(mirror.subs(x,point),y)[0]-y_sol)#adds the y ordinate of the reflected point to the list

    if right_x_sols:#if there are any x solutions on the right
        print("right x")
        if right_m_sols:#if there are any mirror intercepts on the right
            print("right m")
            close_m_right = min(right_m_sols)#take the closest mirror solution
            for sol in right_x_sols:#for each x solution on the left
                if sol > close_m_right:#if it is closer than the mirror solution it is a valid solution
                    print(sol)
                    max_x = check_new_minormax(max_x,sol,"max")
                    y_sol = sym.solve(obj.subs(x,sol),y)[0]#the y solution to the intercept
                    x_coords.append(2*point-sol)#adds the x ordinate of the reflected point to the list
                    y_coords.append(2*sym.solve(mirror.subs(x,point),y)[0]-y_sol)#adds the y ordinate of the reflected point to the list
        else:#if there aren't any mirror solutions on the left then all x solutions are valid for the right
            print("no right m")
            for sol in right_x_sols:#for each x solution on the right
                print(sol)
                max_x = check_new_minormax(max_x,sol,"max")
                y_sol = sym.solve(obj.subs(x,sol),y)[0]#the y solution to the intercept
                x_coords.append(2*point-sol)#adds the x ordinate of the reflected point to the list
                y_coords.append(2*sym.solve(mirror.subs(x,point),y)[0]-y_sol)#adds the y ordinate of the reflected point to the list
    return x_coords,y_coords,max_x,min_x

def check_new_minormax(curr_val,new_val,type):#checks a new minimum or maximumm value and returns the new value
    if type == "max":
        if new_val > curr_val:
            return new_val
    elif type == "min":
        if new_val < curr_val:
            return new_val
    else:
        print("ERROR: invalid type, should be min/max")
    return curr_val

#the matlplotlib setup for the mirror line 
x_coord = np.linspace(-5,5,1111)#sets the bounds for the drawn line and the number of points calculated (precision)
y_coord = []
for i in x_coord:
    y_coord.append(sym.solve(mirror.subs(x,i),y))#calculates the y-coords for each x value of the mirror



#the lists to store the coordinates of the reflected graph
x_coords = []
y_coords = []

#the values for the most distant points the the object is reflected from, starts at infinity so that bounds will be set immediately
min_x = math.inf
max_x = -math.inf

for point in x_coord:#iterates through each point on the mirror line
    gradient = -1/sym.solve(mirror_dx.subs(x,point),y)[0]#gradient of the normal to the mirror at point p
    light_beam = gradient*(x-point)+sym.solve(mirror.subs(x,point),y)[0]#the equation for the line normal to the mirror at point p, the 'light beam'
    solutions = sym.solve(light_beam-sym.solve(obj,y)[0],x)#provides the x-solutions for the light beam and the object
    print("\nPoint")
    print(point)
    print(solutions)

    if solutions:#if there are any solutions in the first place
        x_coords,y_coords,max_x,min_x = validate_solutions(point,solutions,x_coords,y_coords,max_x,min_x)

print(min_x)
print(max_x)
min_x = min_x // 1#rounds down
max_x = max_x // 1 + 1#rounds up

#plot the coords for the object line in order to show all of it that was reflected
#the matlplotlib setup for the object line 
choice = input("Enter manual bounds? y/n")
if choice == "y":
    min_x = int(input("Enter lower x bound: "))
    max_x = int(input("Enter upper x bound: "))

print(max_x)
print(min_x)
precision = 8*math.sqrt(max_x-min_x).__round__()+10

x2_coord = np.linspace(min_x,max_x, precision)#sets the bounds for the drawn line and the number of points calculated (precision)
y2_coord = []
for i in x2_coord:
    y2_coord.append(sym.solve(obj.subs(x,i),y))#calculates the y-coords for each x value of the object


#plot the three graphs
fig, ax = plt.subplots()

new_x2_coord = []
new_y2_coord = []
for i in range(len(x2_coord)):
    if x2_coord[i] and y2_coord[i]:
        new_x2_coord.append(x2_coord[i])
        new_y2_coord.append(y2_coord[i])
ax.plot(new_x2_coord,new_y2_coord,'c')#object

ax.plot(x_coords,y_coords,'b.')#reflection
ax.plot(x_coord, y_coord,'r.')#mirror
ax.plot()
plt.show()

