# import all bullshit
import functools
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")


# Function to create a pie chart with random data
@functools.lru_cache(maxsize=None)
def create_pie_chart(title):
    plt.rcParams['text.color'] = '#c7d5e0'
    fig = Figure(facecolor='#2a475e')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#232323')
    ax.set_title(title)
    labels = ['A', 'B', 'C', 'D', 'E']
    values = [random.randint(1, 100) for x in range(5)]
    plt.style.use('dark_background')
    ax.pie(values, labels=labels, colors=['#1b2838', 'black', '#c7d5e0', '#66c0f4', '#171a21'])
    return fig


# Function to create a bar chart with random data
@functools.lru_cache(maxsize=None)
def create_bar_chart(title):
    plt.rcParams['text.color'] = '#c7d5e0'
    fig = Figure(facecolor='#2a475e')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#232323')
    x_values = range(1, 11)
    y_values = [random.randint(1, 100) for x in range(1, 11)]
    ax.bar(x_values, y_values)
    ax.set_title(title)
    return fig


def create_gui():
    # Create root frame
    root = tk.Tk()
    root.title("Steam dashboard")
    root.configure(bg='#1b2838')

    # Create a frame for the top bar with a title
    top_bar = tk.Frame(root, bg='#1e1e1e', height=50)
    top_bar.grid(row=0, column=1, columnspan=4, sticky="we")
    top_bar.grid_columnconfigure(2, weight=1)

    title_label = tk.Label(top_bar, text="Steam Dashboard", font=("Helvetica", 16), fg="white", bg='#1e1e1e', anchor=tk.CENTER)
    title_label.grid(row=0, column=2, pady=5)

    # Create a bar next to the top bar with 'Friends'
    friend_bar = tk.Frame(root, bg='#1e1e1e', height=50)
    friend_bar.grid(row=0, column=0, columnspan=1, sticky="we")
    friend_bar.grid_columnconfigure(2, weight=1)

    friend_label = tk.Label(friend_bar, text="Friends", font=("Helvetica", 16), fg="white", bg='#1e1e1e', anchor=tk.CENTER)
    friend_label.grid(row=0, column=2, pady=5)

    # Create a frame for the listbox
    listbox_frame = tk.Frame(root, bg='#232323')
    listbox_frame.grid(row=1, column=0, rowspan=3, padx=0, pady=0, sticky='ns')

    # Create a filled listbox
    listbox = tk.Listbox(listbox_frame, bg='#232323', fg='white', selectmode='browse', font=('Helvetica,',20))
    listbox.config(highlightthickness=0)
    listbox.pack(side='left', fill='y')
    for i in range(10):
        listbox.insert(tk.END, f'Friend {i + 1}')

    # Create all 6 data frames and fill them with graphs
    frame1 = tk.Frame(root)
    frame1.grid(row=1, column=1, padx=20, pady=20)
    fig1 = create_pie_chart('Piechart 1')
    canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.LEFT)

    frame2 = tk.Frame(root)
    frame2.grid(row=1, column=2, padx=20, pady=20)
    fig2 = create_bar_chart('Barchart 1')
    canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.LEFT)

    frame3 = tk.Frame(root)
    frame3.grid(row=1, column=3, padx=20, pady=20)
    fig3 = create_bar_chart('Barchart 2')
    canvas3 = FigureCanvasTkAgg(fig3, master=frame3)
    canvas3.draw()
    canvas3.get_tk_widget().pack(side=tk.LEFT)

    frame4 = tk.Frame(root)
    frame4.grid(row=2, column=1, padx=20, pady=20)
    fig4 = create_pie_chart('piechart 2')
    canvas4 = FigureCanvasTkAgg(fig4, master=frame4)
    canvas4.draw()
    canvas4.get_tk_widget().pack(side=tk.LEFT)

    frame5 = tk.Frame(root)
    frame5.grid(row=2, column=2, padx=20, pady=20)
    fig5 = create_pie_chart('Piechart 3')
    canvas5 = FigureCanvasTkAgg(fig5, master=frame5)
    canvas5.draw()
    canvas5.get_tk_widget().pack(side=tk.LEFT)

    frame6 = tk.Frame(root)
    frame6.grid(row=2, column=3, padx=20, pady=20)
    fig6 = create_pie_chart('Piechart 4')
    canvas6 = FigureCanvasTkAgg(fig6, master=frame6)
    canvas6.draw()
    canvas6.get_tk_widget().pack(side=tk.LEFT)

    root.mainloop()


create_gui()
