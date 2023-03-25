import numpy as np
import time
import sys
import random
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk


MAZE_LEN = 500
CNT = 20
UNIT = MAZE_LEN // CNT
cars_cnt = 1
colors = {
    'stone': 'black',
    'space': 'white',
    'car': 'red',
    'destination': 'green'
}

class car():
    def __init__(self):
        self.now_x = 0
        self.now_y = 0
        self.target_x = 0
        self.target_y = 0
        self.direction = ''
        self.speed = 1


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['left', 'right', 'up', 'down']
        self.n_actions = len(self.action_space)
        self.title('maze')
        self.geometry('{0}x{1}'.format(MAZE_LEN, MAZE_LEN))
        self.block_prob = 0.2
        self.maps = [['' for x in range(CNT)] for y in range(CNT)]
        self.cars = [car() for i in range(cars_cnt)]

    def _build_maze(self):
        for i in range(CNT):
            for j in range(CNT):
                val = ''
                if random.random() < self.block_prob:
                    label_frame = tk.Frame(self, width = UNIT, height = UNIT, bg = colors['stone'])
                    val = 'stone'
                else:
                    label_frame = tk.Frame(self, width = UNIT, height = UNIT, bg = colors['space'])
                    val = 'space'
                label_frame.place(x = MAZE_LEN / CNT * i, y = MAZE_LEN / CNT * j)
                self.maps[j][i] = val
    
    def _build_cars(self):
        for ind in range(len(self.cars)):
            self.cars[ind].now_x, self.cars[ind].now_y = self._get_space_point()
            while True:
                x, y = self._get_space_point()
                if x != self.cars[ind].now_x or y != self.cars[ind].now_y:
                    self.cars[ind].target_x = x
                    self.cars[ind].target_y = y
                    break

    def _color_car_and_destination(self):
        print ('car\t', self.cars[0].now_y, self.cars[0].now_x)
        label_frame = tk.Frame(self, width = UNIT, height = UNIT, bg = colors['car'])
        label_frame.place(x = self.cars[0].now_y * UNIT, y = self.cars[0].now_x * UNIT)

        print ('destination\t', self.cars[0].target_y, self.cars[0].target_x)
        label_frame = tk.Frame(self, width = UNIT, height = UNIT, bg = colors['destination'])
        label_frame.place(x = self.cars[0].target_y * UNIT, y = self.cars[0].target_x * UNIT)
    
    def _get_space_point(self):
        while True:
            x = random.randint(0, CNT)
            y = random.randint(0, CNT)
            try:
                if self.maps[x][y] == 'space': 
                    return x, y
            except:
                print ('error', x, y)

    def reset(self):
        self.update()
        time.sleep(0.5)
        self._build_maze()
        self._build_cars()
        self._color_car_and_destination()
        return (self.cars[0].now_x, self.cars[0].now_y, self.cars[0].target_x, self.cars[0].target_y)

    def next_point(self, action, x, y):
        if action == 'up':   # up
            x -= 1
        elif action == 'down':   # down
            x += 1
        elif action == 'left':   # left
            y -= 1 
        elif action == 'right':   # right
            y += 1
        else:
            print ('error: action={} is invalid'.format(action), type(action))
        return (x, y)
    
    def check_action_is_valid(self, ind, action):
        action = self.action_space[int(action)]
        new_x, new_y = self.next_point(action, self.cars[ind].now_x, self.cars[ind].now_y)
        if new_x >= 0 and new_x < CNT and new_y >= 0 and new_y < CNT \
                and self.maps[new_x][new_y] != 'stone':
            return True
        else:
            return False

    def step(self, ind, action):
        action = self.action_space[int(action)]
        label_frame = tk.Frame(self, width = UNIT, height = UNIT, bg = colors['space'])
        label_frame.place(x = self.cars[ind].now_y * UNIT, y = self.cars[ind].now_x * UNIT)
        new_x, new_y = self.next_point(action, self.cars[ind].now_x, self.cars[ind].now_y)

        self.cars[ind].now_x, self.cars[ind].now_y = new_x, new_y
        label_frame = tk.Frame(self, width = UNIT, height = UNIT, bg = colors['car'])
        label_frame.place(x = self.cars[ind].now_y * UNIT, y = self.cars[ind].now_x * UNIT)

        if self.cars[ind].now_x == self.cars[ind].target_x and self.cars[ind].now_y == self.cars[ind].target_y:
            reward = 10
            done = True
            s_ = 'terminal'
        else:
            reward = -2
            done = False
            now_point = (self.cars[0].now_x, self.cars[0].now_y, self.cars[0].target_x, self.cars[0].target_y)
            s_ = "_".join([str(x) for x in now_point])

        return s_, reward, done

    def render(self):
        time.sleep(0.001)
        self.update()
