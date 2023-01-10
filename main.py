import datetime
import matplotlib.pyplot as plt
import tkinter as tk
import tkinter.ttk as ttk

today = datetime.datetime.today()
py_time = today.strftime("%Y %d %m %T")


# main
main = tk.Tk()
width = main.winfo_screenwidth() * 0.8
height = main.winfo_screenheight() * 0.8
x = (width/2) * 0.235
y = (height/2) * 0.2
main.geometry("%dx%d+%d+%d" % (width, height, x, y))
main.configure(bg='#1b2838')

greeting = tk.Label(
    text="hello tkinter",
    bg="#1b2850",
    fg="white",
    height=10,
    width=40
)

greeting.pack()
main.mainloop()
