#!/usr/bin/python3
'''
    support refresh
'''
import tkinter
import tkinter as tk
import random

index = 0
window = tkinter.Tk()

def demo1():
    height = 800
    width = 800
    window.geometry('{}x{}'.format(width, height))
    global index 
    index += 1
    cnt = 3
    for i in range(cnt):
        for j in range(cnt):
            index += 1
            if index % 2 == 0:
                tkinter.Label(window, bg='green').grid(row = j, column = i)
            else:
                tkinter.Label(window, bg='red').grid(row = j, column = i)
    window.after(1000, demo1)


def demo2_frame():
    MAZE_H = 500  # grid height
    MAZE_W = 500  # grid width
    CNT = 20
    block_prob = 0.5
    window.geometry('{0}x{1}'.format(MAZE_W, MAZE_H))
    for i in range(CNT):
        for j in range(CNT):
            if random.random() < block_prob:
                label_frame = tk.Frame(window, width = MAZE_W // CNT, height = MAZE_H // CNT, bg="black")
            else:
                label_frame = tk.Frame(window, width = MAZE_W // CNT, height = MAZE_H // CNT, bg="white")
            label_frame.place(x = MAZE_W / CNT * i, y = MAZE_W / CNT * j)

# demo1()
demo2_frame()
window.mainloop()
