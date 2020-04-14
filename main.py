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
    c_values = [(1,0,0),(1,0,0)]

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
        steps = int(t*factor*60)

        # sin_teta = y / distance
        # cos_teta = x / distance

        teta = atan2( y - self.cursor_pos[1], x - self.cursor_pos[0])
        sin_teta = sin(teta)
        cos_teta = cos(teta)

        print('tgt: ', (x, y), ' origin: ', self.cursor_pos, ' angle: ', math.degrees(teta))

        curve_height = random.choices([-1,1])[0] * random.randrange(30,50)


        for i in range(steps)[::-1]:
            curve_x = i/steps
            curve_y = curve(curve_x, curve_height)
            temp_x = curve_x * distance
            temp_y = curve_y

            temp_x -= self.cursor_pos[0]
            temp_y -= self.cursor_pos[1]

            # cache_x = temp_x * cos_teta - (temp_y * sin_teta)
            # cache_y = temp_x * sin_teta + (temp_y * cos_teta)
            cache_x = temp_x
            cache_y = temp_y
            cache_x += self.cursor_pos[0]
            cache_y += self.cursor_pos[1]

            # cache_x += random.randrange(-2,2)
            # cache_y += random.randrange(-2,2)


            cache_x = clamp(cache_x, 1920, 0)
            cache_y = clamp(cache_y, 1080, 0)


            # print((temp_x,temp_y))
            self.x_values.append(cache_x)
            self.y_values.append(1080 -cache_y)
            self.c_values.append((0, i/steps, 1 - i/steps))
            # self.client.mouseMove(int(cache_x), int(cache_y))

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

bot.move(1920, 1080)

# bot.move(1920, 1000)
# time.sleep(.5)
# bot.move(30, 30)

plt.scatter(bot.x_values, bot.y_values, c=bot.c_values)

plt.show()

