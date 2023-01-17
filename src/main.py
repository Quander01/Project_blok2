# import all bullshit
import functools, tkinter as tk, matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from AI import Ai
matplotlib.use("TkAgg")

root = tk.Tk()
screen_height = int((root.winfo_screenheight())/1.5)
screen_width = int(screen_height*16/9)
print(screen_height)
root.geometry("{}x{}".format(screen_width, screen_height))
print("{}x{}".format(int(screen_height*16/9), screen_height))
text_colour = '#c7d5e0' #slightly blue white-ish
background_colour = '#1b2838' #steam dark blue
figure_colour = '#2a475e' #steam blue
backboard_colour = '#232323' #steam dark grey
highlight_colour = '#66c0f4' #steam light blue
graph_frame_padx = screen_width/170.6
graph_frame_pady = screen_height/96
general_font = 'Arial'
plt.rcParams['text.color'] = text_colour
px = 1/plt.rcParams['figure.dpi']

# Function to open the info windows when clicking on charts
# Only returns "you clicked on..." for now
def on_click(fig, title, event):
    print("you clicked on", title)


# Register when the cursor enters the chart area and change the colour
def on_enter(fig, canvas, event):
    fig.set_facecolor(highlight_colour)
    canvas.draw()


# Register when the cursor leaves the chart area and change the colour back accordingly
def on_leave(fig, canvas, event):
    fig.set_facecolor(figure_colour)
    canvas.draw()


def show_profile():
    print('you clicked on the profile button')
    return


def find_friends(friends_list):
    friends_dict = Ai.friendlistData(Ai.steamId)
    for i in friends_dict:
        friends_list.insert(tk.END, friends_dict[i]['name'])
    return


# Function takes in three parameters: title of the figure, axis names and data to display.
# It creates and returns a pie chart using the matplotlib library.
def create_chart(title, axis, data, chart_type, subplots=111):
    plt.rcParams['text.color'] = text_colour
    fig = Figure(facecolor=figure_colour, figsize=(screen_width/3.8*px, screen_height/2.7*px))
    if chart_type == "progress":
        ax = fig.add_subplot(subplots)
    else:
        ax = fig.add_subplot(111)
    ax.set_facecolor(backboard_colour)
    ax.set_title(title)

    if chart_type == "pie":
        labels = axis
        values = data
        plt.style.use('dark_background')
        ax.pie(values, labels=labels, colors=['#1b2838', 'black', '#c7d5e0', '#66c0f4', '#171a21'])
    elif chart_type == "bar":
        x_values = axis
        y_values = data
        ax.bar(x_values, y_values)
    elif chart_type == "progress":
        ax.set_xlim([0, 100])
        ax.set_yticks([])
        rect = plt.Rectangle((0, 0), data, 1, color=highlight_colour)
        ax.add_patch(rect)
    else:
        raise ValueError("Invalid chart type")
    return fig


# Sends the title, plot data and axis titles to the pie chart creator
# Makes a canvas on the current frame ID
# Assigns usage of on_click and mouseover functions
# Then draws the canvas
def initiate_pie_chart(title, plot_data, axis_titles, frame):
    fig = create_chart(title, axis_titles, plot_data, "pie")
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas.get_tk_widget().bind("<Configure>", lambda event: canvas.draw())
    fig.canvas.mpl_connect('button_press_event', functools.partial(on_click, fig, title))
    canvas.get_tk_widget().bind("<Enter>", functools.partial(on_enter, fig, canvas))
    canvas.get_tk_widget().bind("<Leave>", functools.partial(on_leave, fig, canvas))
    canvas.draw()


# Sends the title, plot data and axis titles to the bar chart creator
# Makes a canvas on the current frame ID
# Assigns usage of on_click and mouseover functions
# Then draws the canvas
def initiate_bar_chart(title, plot_data, axis_titles, frame):
    fig = create_chart(title, axis_titles, plot_data, "bar")
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas.get_tk_widget().bind("<Configure>", lambda event: canvas.draw())
    fig.canvas.mpl_connect('button_press_event', functools.partial(on_click, fig, title))
    canvas.get_tk_widget().bind("<Enter>", functools.partial(on_enter, fig, canvas))
    canvas.get_tk_widget().bind("<Leave>", functools.partial(on_leave, fig, canvas))
    canvas.draw()


# Sends the title and percentage to the progress bar creator
# Makes a canvas on the current frame ID
# Assigns usage of on_click and mouseover functions
# Then draws the canvas
def initiate_progress_bar(title, percentage, frame):
    fig = create_chart(title,'NONE', percentage, "progress", 513)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas.get_tk_widget().bind("<Configure>", lambda event: canvas.draw())
    fig.canvas.mpl_connect('button_press_event', functools.partial(on_click, fig, title))
    canvas.get_tk_widget().bind("<Enter>", functools.partial(on_enter, fig, canvas))
    canvas.get_tk_widget().bind("<Leave>", functools.partial(on_leave, fig, canvas))
    canvas.draw()


# Makes the root gui frames, top bar with title, profile button, friends list and under frame
def gui():
    root.title("Steam dashboard")
    root.configure(bg=background_colour)
    root.resizable(False, False)
    for i in range(4):
        root.grid_columnconfigure(i, weight=1)
        root.grid_rowconfigure(i, weight=1)

    # TITLE BAR
    title_bar = tk.Frame(root, bg=backboard_colour)
    title_bar.grid(row=0, column=1, columnspan=3, sticky="wsne")
    title_bar.grid_columnconfigure(2, weight=1)

    title_label = tk.Label(title_bar, text="Steam Dashboard", font=(general_font, 30), fg=text_colour, bg=backboard_colour, anchor=tk.CENTER)
    title_label.grid(row=0, column=2, pady=screen_height/19.2)

    # PROFILE BUTTON
    profile_bar = tk.Frame(root, bg=backboard_colour)
    profile_bar.grid(row=0, column=0, columnspan=1, rowspan=6, sticky="news")

    profile_button = tk.Button(profile_bar, text="Profile", font=(general_font, 18), fg=text_colour, bg=backboard_colour, anchor=tk.CENTER, command=show_profile, height=5)
    profile_button.grid(sticky="news")

    # FRIENDS LIST
    listbox_frame = tk.Frame(root, bg=backboard_colour)
    listbox_frame.grid(row=2, column=0, rowspan=3, sticky='news', padx=screen_width/113)

    friends_list = tk.Listbox(listbox_frame, bg=backboard_colour, fg=text_colour, selectmode='single', font=(general_font, 17), selectbackground=highlight_colour, selectforeground='Black', activestyle='none')
    friends_list.config(highlightthickness=0)
    friends_list.pack(side='left', fill='y')
    find_friends(friends_list)
    listbox_width = friends_list.cget("width")
    profile_button.config(width=listbox_width)

    # BOTTOM FRAME
    bottom_frame = tk.Frame(root, bg=backboard_colour,)
    bottom_frame.grid(row=4, column=1, columnspan=3, sticky='news')

    under_text = tk.Label(bottom_frame, text='hello there', bg=backboard_colour, fg=text_colour, font=(general_font, 20))
    under_text.pack(side='left')
    frames()


# Graph frames are created and data sent to the initiators
def frames():
    frame1 = tk.Frame(root)
    frame1.grid(row=2, column=1, padx=graph_frame_padx, pady=graph_frame_pady)
    initiate_pie_chart("pie chart demo 1", (1, 2, 3, 4, 5), ('A', 'B', 'C', 'D', 'E'), frame1)

    frame2 = tk.Frame(root)
    frame2.grid(row=2, column=2, padx=graph_frame_padx, pady=graph_frame_pady)
    initiate_bar_chart("bar chart demo 1", (1, 2, 3, 4, 5), ('A', 'B', 'C', 'D', 'E'), frame2)

    frame3 = tk.Frame(root)
    frame3.grid(row=2, column=3, padx=graph_frame_padx, pady=graph_frame_pady)
    initiate_bar_chart("bar chart demo 2", (3, 2, 3, 4, 3), ('A', 'B', 'C', 'D', 'E'), frame3)

    frame4 = tk.Frame(root)
    frame4.grid(row=3, column=1, padx=graph_frame_padx, pady=graph_frame_pady)
    initiate_pie_chart("pie chart demo 2", (4, 2, 4, 4, 5), ('A', 'B', 'C', 'D', 'E'), frame4)

    frame5 = tk.Frame(root)
    frame5.grid(row=3, column=2, padx=graph_frame_padx, pady=graph_frame_pady)
    initiate_pie_chart("pie chart demo 3", (1, 2, 5, 4, 5), ('A', 'B', 'C', 'D', 'E'), frame5)

    frame6 = tk.Frame(root)
    frame6.grid(row=3, column=3, padx=graph_frame_padx, pady=graph_frame_pady)
    initiate_progress_bar("progress bar demo", 23, frame6)


gui()
root.mainloop()
