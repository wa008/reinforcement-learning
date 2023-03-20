#!/usr/bin/python3
'''
    support refresh
'''
import tkinter

window = tkinter.Tk()
height = 800
width = 800
window.geometry('{}x{}'.format(width, height))
index = 0

def run():
    global index 
    index += 1
    cnt = 3
    for i in range(cnt):
        for j in range(cnt):
            if index % 2 == 0:
                tkinter.Label(window, bg='green', width = 10, height = 5).grid(row = j, column = i)
            else:
                tkinter.Label(window, bg='red', width = 10, height = 5).grid(row = j, column = i)
    window.after(1000, run)

run()
window.mainloop()
