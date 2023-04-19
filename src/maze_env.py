import numpy as np
import time
import sys
import random
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk
import copy


MAZE_LEN = 500
CNT = 20
UNIT = MAZE_LEN // CNT
cars_cnt = 5
colors = {
    'stone': 'black',
    'space': 'white',
    'car': 'red',
    'destination': 'yellow',
    'done': 'green'
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
        self.action_space = ['left', 'right', 'up', 'down', 'stay']
        self.n_actions = len(self.action_space)
        self.title('maze')
        self.geometry('{0}x{1}'.format(MAZE_LEN, MAZE_LEN))
        self.block_prob = 0.2
        self.maps = [['' for x in range(CNT)] for y in range(CNT)]
        self.cars = [car() for i in range(cars_cnt)]
        self.cars_set = set()

    def _build_maze_space_row(self, ind):
        for j in range(CNT):
            self.maps[ind][j] = 'space'
            
    def _build_maze_space_col(self, ind):
        for i in range(CNT):
            self.maps[i][ind] = 'space'
            
    def _build_maze(self):
        for i in range(CNT):
            for j in range(CNT):
                self.maps[i][j] = 'stone'
        
        base_row = 0
        while base_row < CNT:
            self._build_maze_space_row(base_row)
            base_row += random.randint(3, 5)
    
        base_col = 0
        while base_col < CNT:
            self._build_maze_space_col(base_col)
            base_col += random.randint(3, 5)

        for i in range(CNT):
            for j in range(CNT):
                label_frame = tk.Frame(self, width = UNIT, height = UNIT, bg = colors[self.maps[j][i]])
                label_frame.place(x = MAZE_LEN / CNT * i, y = MAZE_LEN / CNT * j)
                
    def _build_cars(self):
        for ind in range(len(self.cars)):
            self.cars[ind].now_x, self.cars[ind].now_y = self._get_space_point()
            self.cars[ind].target_x, self.cars[ind].target_y = self._get_space_point()
            self.maps[self.cars[ind].target_x][self.cars[ind].target_y] = 'destination'

    def _color_car_and_destination(self):
        for car in self.cars:
            label_frame = tk.Frame(self, width = UNIT, height = UNIT, bg = colors['car'])
            label_frame.place(x = car.now_y * UNIT, y = car.now_x * UNIT)

            label_frame = tk.Frame(self, width = UNIT, height = UNIT, bg = colors['destination'])
            label_frame.place(x = car.target_y * UNIT, y = car.target_x * UNIT)
    
    def _get_space_point(self):
        while True:
            x = random.randint(0, CNT - 1)
            y = random.randint(0, CNT - 1)
            try:
                if self.maps[x][y] == 'space' and (x, y) not in self.cars_set:
                    self.cars_set.add((x, y))
                    return x, y
            except:
                print ('error', x, y)
    
    def _get_observation(self, ind):
        point = [self.cars[ind].now_x, self.cars[ind].now_y, self.cars[ind].target_x, self.cars[ind].target_y]
        observation = "_".join([str(x) for x in point])
        return observation

    def reset(self):
        self.update()
        time.sleep(0.5)
        self._build_maze()
        self._build_cars()
        self._color_car_and_destination()

    def next_point(self, action, x, y):
        if action == 'up':   # up
            x -= 1
        elif action == 'down':   # down
            x += 1
        elif action == 'left':   # left
            y -= 1 
        elif action == 'right':   # right
            y += 1
        elif action == 'stay':
            pass 
        else:
            print ('error: action={} is invalid'.format(action), type(action))
        return (x, y)
    
    def all_action_is_valid(self, action_list):
        cars = copy.deepcopy(self.cars)
        cars_set = set()
        for ind in range(len(self.cars)):
            # RL take action and get next observation and reward
            action = action_list[ind]
            action = self.action_space[int(action)]
            cars[ind].now_x, cars[ind].now_y = self.next_point(action, cars[ind].now_x, cars[ind].now_y)
            if (cars[ind].now_x, cars[ind].now_y) in cars_set:
                return False
            else:
                cars_set.add((cars[ind].now_x, cars[ind].now_y))
        return True

    def check_action_is_valid(self, ind, action):
        action = self.action_space[int(action)]
        new_x, new_y = self.next_point(action, self.cars[ind].now_x, self.cars[ind].now_y)
        if new_x >= 0 and new_x < CNT and new_y >= 0 and new_y < CNT \
                and self.maps[new_x][new_y] in ('space', 'destination'):
            return True
        else:
            return False

    def debug_cars(self, ind):
        print ('cars: {}\t{}\t{}\t{}\n'.format(self.cars[ind].now_x, self.cars[ind].now_y, self.cars[ind].target_x, self.cars[ind].target_y))

    def check_is_sucess(self, ind):
        if self.cars[ind].now_x == self.cars[ind].target_x and self.cars[ind].now_y == self.cars[ind].target_y:
            return True
        else:
            return False

    def step(self, ind, action):
        if self.check_is_sucess(ind):
            reward = 10
            done = True
            s_ = 'terminal'
            return s_, reward, done
        action = self.action_space[int(action)]
        color = colors[self.maps[self.cars[ind].now_x][self.cars[ind].now_y]]
        label_frame = tk.Frame(self, width = UNIT, height = UNIT, bg = color)
        label_frame.place(x = self.cars[ind].now_y * UNIT, y = self.cars[ind].now_x * UNIT)
        new_x, new_y = self.next_point(action, self.cars[ind].now_x, self.cars[ind].now_y)

        self.cars[ind].now_x, self.cars[ind].now_y = new_x, new_y
        label_frame = tk.Frame(self, width = UNIT, height = UNIT, bg = colors['car'])
        label_frame.place(x = self.cars[ind].now_y * UNIT, y = self.cars[ind].now_x * UNIT)

        if self.check_is_sucess(ind):
            reward = 10
            done = True
            s_ = 'terminal'
            self.maps[self.cars[ind].now_x][self.cars[ind].now_y] = 'done'
            label_frame = tk.Frame(self, width = UNIT, height = UNIT, bg = colors['done'])
            label_frame.place(x = self.cars[ind].now_y * UNIT, y = self.cars[ind].now_x * UNIT)
        else:
            reward = -2
            done = False
            now_point = (self.cars[ind].now_x, self.cars[ind].now_y, self.cars[ind].target_x, self.cars[ind].target_y)
            s_ = "_".join([str(x) for x in now_point])

        return s_, reward, done

    def render(self):
        time.sleep(0.001)
        self.update()
