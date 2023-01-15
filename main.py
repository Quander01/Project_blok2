# import all bullshit
import functools
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")

root = tk.Tk()


# function to open the info windows when clicking on charts
def on_click(fig, event):
    print("you clicked")


# register when the cursor enters the chart area and change the colour
def on_enter(fig, canvas, event):
    fig.set_facecolor('#66c0f4')
    canvas.draw()


# register when the cursor leaves the chart area and change the colour back accordingly
def on_leave(fig, canvas, event):
    fig.set_facecolor('#2a475e')
    canvas.draw()


# Function to create a pie chart
def create_pie_chart(title, axis, data):
    plt.rcParams['text.color'] = '#c7d5e0'
    fig = Figure(facecolor='#2a475e')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#232323')
    ax.set_title(title)
    labels = axis
    values = data
    plt.style.use('dark_background')
    ax.pie(values, labels=labels, colors=['#1b2838', 'black', '#c7d5e0', '#66c0f4', '#171a21'])
    return fig


# Function to create a bar chart
def create_bar_chart(title, axis, data):
    plt.rcParams['text.color'] = '#c7d5e0'
    fig = Figure(facecolor='#2a475e')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#232323')
    x_values = axis
    y_values = data
    ax.bar(x_values, y_values)
    ax.set_title(title)
    return fig


# send the data to the piechart creator and configure the returned chart
def initiate_pie_chart(title, plot_data, axis_titles, frame):
    fig = create_pie_chart(title, axis_titles, plot_data)
    fig.canvas.mpl_connect('button_press_event', functools.partial(on_click, fig))
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().bind("<Enter>", functools.partial(on_enter, fig, canvas))
    canvas.get_tk_widget().bind("<Leave>", functools.partial(on_leave, fig, canvas))
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# send the data to the barchart creator and configure the returned chart
def initiate_bar_chart(title, plot_data, axis_titles, frame):
    fig = create_bar_chart(title, axis_titles, plot_data)
    fig.canvas.mpl_connect('button_press_event', on_click)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().bind("<Enter>", functools.partial(on_enter, fig, canvas))
    canvas.get_tk_widget().bind("<Leave>", functools.partial(on_leave, fig, canvas))
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT)


# make the gui frames and anything that does not change
def gui():
    root.title("Steam dashboard")
    root.configure(bg='#1b2838')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    # Create a frame for the top bar with a title
    top_bar = tk.Frame(root, bg='#1e1e1e', height=50)
    top_bar.grid(row=0, column=1, columnspan=4, sticky="we")
    top_bar.grid_columnconfigure(2, weight=1)

    title_label = tk.Label(top_bar, text="Steam Dashboard", font=("Arial", 16), fg="white", bg='#1e1e1e', anchor=tk.CENTER)
    title_label.grid(row=0, column=2, pady=5)

    # Create a bar next to the top bar with 'Friends'
    friend_bar = tk.Frame(root, bg='#1e1e1e', height=50)
    friend_bar.grid(row=0, column=0, columnspan=1, sticky="we")
    friend_bar.grid_columnconfigure(2, weight=1)

    friend_label = tk.Label(friend_bar, text="Friends", font=("Arial", 16), fg="white", bg='#1e1e1e', anchor=tk.CENTER)
    friend_label.grid(row=0, column=2, pady=5)

    # Create a frame for the listbox
    listbox_frame = tk.Frame(root, bg='#232323')
    listbox_frame.grid(row=1, column=0, rowspan=3, padx=0, pady=0, sticky='ns')

    # Create a filled listbox
    listbox = tk.Listbox(listbox_frame, bg='#232323', fg='white', selectmode='browse', font=('Helvetica', 20))
    listbox.config(highlightthickness=0)
    listbox.pack(side='left', fill='y')
    for i in range(10):
        listbox.insert(tk.END, f'Friend {i + 1}')
    frames()


# here the frames are called and given data
def frames():
    frame1 = tk.Frame(root)
    frame1.grid(row=1, column=1, padx=20, pady=20)
    initiate_pie_chart("test", (1, 2, 3, 4, 5), ('A', 'B', 'C', 'D', 'E'), frame1)

    frame2 = tk.Frame(root)
    frame2.grid(row=1, column=2, padx=20, pady=20)
    initiate_bar_chart("test2", (1, 2, 3, 4, 5), ('A', 'B', 'C', 'D', 'E'), frame2)

    frame3 = tk.Frame(root)
    frame3.grid(row=1, column=3, padx=20, pady=20)
    initiate_bar_chart("test3", (1, 2, 3, 4, 5), ('A', 'B', 'C', 'D', 'E'), frame3)

    frame4 = tk.Frame(root)
    frame4.grid(row=2, column=1, padx=20, pady=20)
    initiate_pie_chart("test4", (1, 2, 3, 4, 5), ('A', 'B', 'C', 'D', 'E'), frame4)

    frame5 = tk.Frame(root)
    frame5.grid(row=2, column=2, padx=20, pady=20)
    initiate_pie_chart("test5", (1, 2, 3, 4, 5), ('A', 'B', 'C', 'D', 'E'), frame5)

    frame6 = tk.Frame(root)
    frame6.grid(row=2, column=3, padx=20, pady=20)
    initiate_pie_chart("test6", (1, 2, 3, 4, 5), ('A', 'B', 'C', 'D', 'E'), frame6)


gui()
root.mainloop()
