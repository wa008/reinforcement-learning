#!/usr/bin/python3
 
import tkinter

window = tkinter.Tk()
height = 800
width = 800
window.geometry('{}x{}'.format(width, height))
cnt = 3
for i in range(cnt):
    for j in range(cnt):
        print (i, j)
        tkinter.Label(window, bg='green', width = 10, height = 5).grid(row = j, column = i)

window.mainloop()
