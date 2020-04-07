from vncdotool import api
import time
import random
import json

class Bot():
    def __init__(self):
        with open('config.json') as file:
            self.credentials = json.load(file)
        self.client = api.connect('192.168.8.102', self.credentials['system_password'])

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

    def game_login(self):
        print('Game login...')
        pswd = self.credentials['tibia_password']
        for k in pswd:
            time.sleep(random.random()/10 + 0.1)
            self.client.keyPress(k)

        self.client.keyPress('enter')
        time.sleep(2)
        self.client.keyPress('enter')

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
bot.system_login()