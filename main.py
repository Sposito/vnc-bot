from vncdotool import api
import time
import random
import json
import matplotlib.pyplot as plt
import numpy as np
from math import atan2, sin, cos, degrees
import math

class Bot():
    def __init__(self):
        with open('config.json') as file:
            self.credentials = json.load(file)
        self.client = api.connect('192.168.8.102', self.credentials['system_password'])
        self.cursor_pos = (0,0)
        self.client.mouseMove(*self.cursor_pos)

    def system_login(self):
        self.client
        print('System login...')

        for k in self.credentials['system_password']:
            self.client.keyPress(k)

        self.client.keyPress('enter')
        time.sleep(2)

    def game_launch(self):
        print('Launching game...')
        combo = ['ctrl', 'alt', 't']

        for k in combo:
            self.client.keyDown(k)
        for k in combo[::-1]:
            self.client.keyUp(k)

        time.sleep(2)
        cmd = '~/Tibia/Tibia'

        for k in cmd:
            self.client.keyPress(k)

        self.client.keyPress('enter')
        time.sleep(5)
        self.clientmouseMove(self.cursor_pos)

    def game_login(self):
        print('Game login...')
        pswd = self.credentials['tibia_password']
        for k in pswd:
            time.sleep(random.random()/10 + 0.1)
            self.client.keyPress(k)

        self.client.keyPress('enter')
        time.sleep(2)
        self.client.keyPress('enter')

    x_values = [0, 1920]
    y_values = [0, 1080]
    c_values = [(1,1,1),(1,1,1)]

    def move(self, x, y, t=100):
        def get_distance(x1, y1, x2, y2):
            return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

        def curve(x, h):
            return 4 * h * x**2 + -4 * h * x

        def clamp(value,max, min=0):
            if value < min:
             return min
            if value > max:
                return max
            return value


        distance = get_distance(x, y, *self.cursor_pos)

        if distance == 0:
            return

        factor = distance / 2203  # diagonal on full hd screen
        steps = int(t*factor*40)

        teta = atan2( y - self.cursor_pos[1], x - self.cursor_pos[0])
        sin_teta = sin(teta)
        cos_teta = cos(teta)

        print('tgt: ', (x, y), ' origin: ', self.cursor_pos, ' angle: ', math.degrees(teta))

        curve_height =  (random.random() - 0.5) * 2

        _x = self.cursor_pos[0]
        _y = self.cursor_pos[1]
        for i in range(steps):
            n = i /steps
            cache_x = x * n + (1 -n) * _x
            cache_y = y * n + (1 -n) * _y

            h =  curve(n, curve_height)

            cache_x += h * sin_teta * distance / 5
            cache_y += h * cos_teta * distance / 5

            cache_x += (random.random()-.5) * 1
            cache_y += (random.random() - .5) * 1

            cache_x = clamp(cache_x, 1920)
            cache_y = clamp(cache_y, 1080)



            # print((temp_x,temp_y))
            self.x_values.append(cache_x)
            self.y_values.append(1080 -cache_y)
            self.c_values.append(( i/steps,0, 1 - i/steps))
            self.client.mouseMove(int(cache_x), int(cache_y))


        self.client.mouseMove(x,y)
        self.cursor_pos = (x, y)




    # i = 0
    # print('Test walk...')
    # for k in 'dddaaadadad':
    #     t = time.time_ns()
    #     client.keyPress(k)
    #     client.captureScreen(f'screenshots/file_{i}.png')
    #     # client.captureRegion(f'screenshots/file_{i}.png', 1024, 600, 30, 60 )
    #     print (f'{i}: ', (time.time_ns() - t)/1000000000)
    #     i += 1

bot = Bot()
# bot.system_login()


# bot.move(0,1080)
# time.sleep(.5)
for i in range(9):
    bot.move(int(random.random() * 1920), int(random.random() * 1080))
    time.sleep(random.random())

# bot.move(1920, 1000)
# time.sleep(.5)
# bot.move(30, 30)

# plt.scatter(bot.x_values, bot.y_values, c=bot.c_values)
#
# plt.show()

