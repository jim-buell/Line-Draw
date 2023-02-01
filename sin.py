import math
import matplotlib.pyplot as plt

xlist = []
ylist = []

def get_sin_wave_points(amplitude, frequency, step, start_offset):
    points = []
    starting_points = [-1000 + start_offset, 0 + start_offset]
    for start in starting_points:
        for i in range(step):
            x = i / step
            y = (amplitude * math.sin(2 * math.pi * frequency * x) + 1240)
            points.append((y, (x * 1000) + start))
            plt.plot(xlist, ylist)
            plt.show()
    #my_line.g01(y, x, 1000) # Lifts the pen at the end of the wave
    return points

def get_sawtooth_wave_points(amplitude, frequency, step):
    points = []
    num_steps = int(1 / frequency / step)
    for i in range(num_steps):
        x = i * step
        y = (amplitude * (2 * (x * frequency - math.floor(x * frequency + 0.5)))) + 1240
        points.append((x, y))
    xlist.append(x)
    ylist.append(y)
    plt.plot(xlist, ylist)
    plt.show()
    return points

# Example usage
amplitude = 20
frequency = 0.25
step = 0.01
points = get_sawtooth_wave_points(amplitude, frequency, step)

print(points)

