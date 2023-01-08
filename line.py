from lineus import LineUs
import time
import math
import random

# ———————— Startup ————————— #

my_line = LineUs()
my_line.connect()
time.sleep(1)

# ——————— Functions ———————— #

def get_circle_points(center, radius, num_points):
    points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    return points

def get_sin_wave_points(amplitude, frequency, step, start_offset):
    points = []
    starting_points = [-1000 + start_offset, 0 + start_offset]
    for start in starting_points:
        for i in range(step):
            x = i / step
            y = (amplitude * math.sin(2 * math.pi * frequency * x) + 1240)
            points.append((y, (x * 1000) + start))
    my_line.g01(y, x, 1000) # Lifts the pen at the end of the wave
    return points

def points_to_gcode(points):
    for entry in points:
        my_line.g01(entry[0], entry[1], 0)
        #print("X = ", entry[0], "Y = ", entry[1])
    #my_line.g01(points[-1][0], points[-1][1], 1000) # Gets the last entry in the drawing and lifts the pen

def circle_spiral(x, y, radius, points, y_increment):
    counter = 0
    until = y
    total_circles = int(abs((abs(y)+abs(until)) / y_increment)) - 20 # Makes a shorter spiral on the "big" side —— ie it subtracts circles from the end. 
    while counter < total_circles:
        points_to_gcode(get_circle_points((x, y), radius, points))
        print("Circle {} of {}.".format((counter + 1), total_circles))
        y += y_increment
        radius += 2 # Make this a smaller number if 
        points += 1
        counter += 1
    my_line.g01(x, y, 1000) # Lifts the pen


def get_sawtooth_wave_points(amplitude, frequency, step, start_offset):
    points = []
    num_steps = int(1 / frequency / step)
    starting_points = [-1000 + start_offset, 0 + start_offset]
    for start in starting_points:
        for i in range(num_steps):
            x = i * step
            y = (amplitude * (2 * (x * frequency - math.floor(x * frequency + 0.5)))) + 1240
            points.append((y, (x * 1000) + start))
    my_line.g01(y, x, 1000) # Lifts the pen at the end of the wave
    return points


# ———————— Patterns ————————— #    

def make_circle_spiral():

    start_x = 950
    finish_x = 1550
    x_increment = 200
    segement_counter = 1

    for x in range(start_x, finish_x, x_increment):
        start_radius = 50
        start_points = 15
        y_start = 700
        y_increment = 10 # Make this bigger to have more space between circles. 
        print("Starting segment {} of {}.".format(segement_counter, 2 * int(((finish_x - start_x) / x_increment))))
        circle_spiral(x, y_start, start_radius, start_points, -y_increment)
        segement_counter += 1
        print("Starting segment {} of {}.".format(segement_counter, 2 * int(((finish_x - start_x) / x_increment))))
        circle_spiral(x, -y_start, start_radius, start_points, y_increment)
        segement_counter += 1


def make_sin_wave():

    counter = 0

    range_start = -99
    range_end = 495
    range_step = 99
    for start in range(range_start, range_end, range_step):

        amp_range_start = 100
        amp_range_end = 540
        amp_range_step = 20

        for amp_range in range(amp_range_start, amp_range_end, amp_range_step):
            amplitude = amp_range # Amplitude between 10 and 540
            frequency = 1 # Frequence between .5 and 20
            start_offset = start
            step = 100
            points = get_sin_wave_points(amplitude, frequency, step, start_offset)

            total_waves = ((range_end - range_start) / range_step) * ((amp_range_end - amp_range_start) / amp_range_step)
            counter += 1
            print("Sine wave {} of {}.".format(counter, int(total_waves)))

            points_to_gcode(points)

def make_sawtooth():
    counter = 0

    range_start = 0
    range_end = 495
    range_step = 99
    adder = 0

    for start in range(range_start, range_end, range_step):

        amp_range_start = 100
        amp_range_end = 340 + adder # adds more apmplitude each pass
        amp_range_step = 20

        for amp_range in range(amp_range_start, amp_range_end, amp_range_step):
            amplitude = amp_range
            frequency = 1
            step = 0.01
            start_offset = start
            points = get_sawtooth_wave_points(amplitude, frequency, step, start_offset)

            total_waves = ((range_end - range_start) / range_step) * ((amp_range_end - amp_range_start) / amp_range_step)
            counter += 1
            print("Sawtooth wave {} of {}.".format(counter, int(total_waves)))

            points_to_gcode(points)
        adder += 40

def make_concentric_circles(): # Makes a series of circles (which are filled in) of random size on random part of the paper. 
    for x in range(0, random.randint(5, 10)): # Defines the number of total circles to make. 
        center = [random.randint(1000, 1600), random.randint(-700, 700)] # Randomly determines where the center is.
        num_points = 50 # Defines the number of points that make up each circle. 
        for radius in range(50, random.randrange(100, 400, 50), 10): # Itereates drawing increasingly-large individual circles in sequence to create filled in circles. 
            points_to_gcode(get_circle_points(center, radius, num_points)) # Calls the circle-creation code and passes it to the Line-US. 
        my_line.g01(center[0], center[1], 1000) # Lifts the pen at the end of filled circle. 

        

# ———————— Script ————————— #    

#make_circle_spiral()
make_sin_wave()
#make_sawtooth()
#make_concentric_circles()

# ———————— Cleanup ————————— #

my_line.disconnect()