import matplotlib.pyplot as plt
import math

def get_sin_wave_points(amplitude, frequency, step, start_offset):
    points = []
    starting_points = [-1000 + start_offset, 0 + start_offset]
    for start in starting_points:
        for i in range(step):
            x = i / step
            y = (amplitude * math.sin(2 * math.pi * frequency * x) + 1240)
            points.append((y, (x * 1000) + start))
    plt.plot(y, x)
    #plt.show()  

def make_sin_wave():

    counter = 0

    range_start = 0
    range_end = 495
    range_step = 99
    for start in range(range_start, range_end, range_step):

        amp_range_start = 100
        amp_range_end = 540
        amp_range_step = 10

        for amp_range in range(amp_range_start, amp_range_end, amp_range_step):
            amplitude = amp_range # Amplitude between 10 and 540
            frequency = 1 # Frequence between .5 and 20
            start_offset = start
            step = 100
            points = get_sin_wave_points(amplitude, frequency, step, start_offset)

            total_waves = ((range_end - range_start) / range_step) * ((amp_range_end - amp_range_start) / amp_range_step)
            counter += 1
            print("Sine wave {} of {}.".format(counter, int(total_waves)))
    plt.show()

make_sin_wave()

