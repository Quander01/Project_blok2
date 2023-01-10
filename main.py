from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")


def create_piechart():
    # Create a new figure
    fig = Figure(facecolor='#2a475e')

    # Add a subplot to the figure
    ax = fig.add_subplot(111)
    ax.set_facecolor('#232323')

    # Generate some random data
    labels = ['A', 'B', 'C', 'D', 'E']
    values = [random.randint(1, 100) for x in range(5)]

    plt.style.use('dark_background')
    plt.rcParams['text.color'] = 'white'

    # Plot the data as a pie chart
    ax.pie(values, labels=labels, colors=['#d50000', '#283593', '#689f38', '#4dd0e1', '#f9a825'])
    ax.set_title('Pie Chart Example')
    # Return the figure object
    return fig


def create_bar_chart():
    fig = Figure(facecolor='#2a475e')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#232323')

    x_values = range(1, 11)
    y_values = [random.randint(1, 100) for x in range(1, 11)]

    plt.style.use('dark_background')
    plt.rcParams['lines.color'] = 'white'
    plt.rcParams['text.color'] = 'white'
    plt.rcParams['axes.labelcolor'] = 'white'
    plt.rcParams['xtick.color'] = 'white'
    plt.rcParams['ytick.color'] = 'white'
    plt.rcParams['grid.color'] = 'white'

    ax.bar(x_values, y_values)
    ax.set_title("Bar Chart Example")
    return fig


def create_list_box():
    listbox_frame = tk.Frame(root, bg='#232323')
    listbox_frame.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky='ns')
    listbox = tk.Listbox(listbox_frame, bg='#232323', fg='white', selectmode='browse')
    listbox.config(highlightthickness=0)
    listbox.pack(side='left', fill='y')
    scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=listbox.yview)
    scrollbar.pack(side='right', fill='y')
    listbox.config(yscrollcommand=scrollbar.set)


def create_progressbar():
    pb_frame = tk.Frame(root, bg='#232323')
    pb_frame.grid(row=1, column=3, padx=10, pady=10)
    pb = ttk.Progressbar(pb_frame, orient='horizontal', length=200, mode='determinate')
    pb.pack()
    return pb


root = tk.Tk()
root.title("Graphs")
root.configure(bg='#1b2838')


# Create a frame for the listbox
listbox_frame = tk.Frame(root, bg='#232323')
listbox_frame.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky='ns')

# Create a listbox and scrollbar
listbox = tk.Listbox(listbox_frame, bg='#232323', fg='white', selectmode='browse')
listbox.config(highlightthickness=0)
listbox.pack(side='left', fill='y')


s = ttk.Style()
s.configure("Vertical.TScrollbar", gripcount=0, background="#232323", troughcolor="#232323", bordercolor="#232323",  arrowcolor="white")
s.configure("Vertical.TScrollbar", lightcolor="grey", darkcolor="white")

scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', style="Vertical.TScrollbar", command=listbox.yview)
scrollbar.pack(side='right', fill='y')
listbox.config(yscrollcommand=scrollbar.set)


frame1 = tk.Frame(root)
frame1.grid(row=0, column=1, padx=20, pady=20)
fig1 = create_piechart()
canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
canvas1.draw()
canvas1.get_tk_widget().pack(side=tk.LEFT)

frame2 = tk.Frame(root)
frame2.grid(row=0, column=2, padx=20, pady=20)
fig2 = create_bar_chart()
canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
canvas2.draw()
canvas2.get_tk_widget().pack(side=tk.LEFT)

frame3 = tk.Frame(root)
frame3.grid(row=0, column=3, padx=20, pady=20)
fig3 = create_piechart()
canvas3 = FigureCanvasTkAgg(fig3, master=frame3)
canvas3.draw()
canvas3.get_tk_widget().pack(side=tk.LEFT)

frame4 = tk.Frame(root)
frame4.grid(row=1, column=1, padx=20, pady=20)
fig4 = create_bar_chart()
canvas4 = FigureCanvasTkAgg(fig4, master=frame4)
canvas4.draw()
canvas4.get_tk_widget().pack(side=tk.LEFT)

frame5 = tk.Frame(root)
frame5.grid(row=1, column=2, padx=20, pady=20)
fig5 = create_piechart()
canvas5 = FigureCanvasTkAgg(fig5, master=frame5)
canvas5.draw()
canvas5.get_tk_widget().pack(side=tk.LEFT)

frame6 = tk.Frame(root)
frame6.grid(row=1, column=3, padx=20, pady=20)
fig6 = create_piechart()
canvas6 = FigureCanvasTkAgg(fig6, master=frame6)
canvas6.draw()
canvas6.get_tk_widget().pack(side=tk.LEFT)

'''
for i in range(6):
    listbox.insert(tk.END, f'Friend {i + 1}')'''

root.mainloop()
