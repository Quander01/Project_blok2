# import all bullshit
import functools
import matplotlib
import tkinter as tk
from webbrowser import open

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from AI import Ai

matplotlib.use("TkAgg")


root = tk.Tk()
screen_height = int(root.winfo_screenheight()/1.2)
screen_width = int(screen_height*16/9)
root.geometry("{}x{}".format(screen_width, screen_height))
text_colour = '#c7d5e0'                                         # slightly blue white-ish
background_colour = '#1b2838'                                   # steam dark blue
figure_colour = '#2a475e'                                       # steam blue
backboard_colour = '#232323'                                    # steam dark grey
highlight_colour = '#66c0f4'                                    # steam light blue
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
    open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return


def find_friends(friends_list):
    friends_dict = Ai.friendlistData(user_id)
    for i in friends_dict:
        friends_list.insert(tk.END, friends_dict[i]['name'])
    return


class CreateCharts:
    def __init__(self, title, data, axis, chart_type, frame, steamid):
        self.steamId = steamid
        self.chart_type = chart_type
        self.title = title
        self.axis = axis
        self.data = data
        self.frame = frame
        if chart_type == "progress":
            self.initiate_progress_bar()
        elif chart_type == "bar":
            self.initiate_bar_chart()
        elif chart_type == "pie":
            self.initiate_pie_chart()

    # Function takes in three parameters: title of the figure, axis names and data to display.
    # It creates and returns a pie chart using the matplotlib library.
    def create_chart(self):
        plt.rcParams['text.color'] = text_colour
        fig = Figure(facecolor=figure_colour, figsize=(screen_width/3.8*px, screen_height/2.7*px))
        if self.chart_type == "progress":
            ax = fig.add_subplot(513)
        else:
            ax = fig.add_subplot(111)
        ax.set_facecolor(backboard_colour)
        ax.set_title(self.title)
        if self.chart_type == "pie":
            labels = self.axis
            values = self.data
            plt.style.use('dark_background')
            ax.pie(values, labels=labels, colors=['#1b2838', 'black', '#c7d5e0', '#66c0f4', '#171a21'])
        elif self.chart_type == "bar":
            x_values = self.axis
            y_values = self.data
            bars = ax.bar(x_values, y_values)
            ax.bar_label(bars)
        elif self.chart_type == "progress":
            ax.set_xlim([0, 100])
            ax.set_yticks([])
            rect = plt.Rectangle((0, 0), self.data, 1, color=highlight_colour)
            ax.add_patch(rect)
        else:
            raise ValueError("Invalid chart type")
        return fig

    # Sends the title, plot data and axis titles to the pie chart creator
    # Makes a canvas on the current frame ID
    # Assigns usage of on_click and mouseover functions
    # Then draws the canvas
    def initiate_pie_chart(self):
        fig = self.create_chart()
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.get_tk_widget().bind("<Configure>", lambda event: canvas.draw())
        fig.canvas.mpl_connect('button_press_event', functools.partial(on_click, fig, self.title))
        canvas.get_tk_widget().bind("<Enter>", functools.partial(on_enter, fig, canvas))
        canvas.get_tk_widget().bind("<Leave>", functools.partial(on_leave, fig, canvas))
        canvas.draw()

    # Sends the title, plot data and axis titles to the bar chart creator
    # Makes a canvas on the current frame ID
    # Assigns usage of on_click and mouseover functions
    # Then draws the canvas
    def initiate_bar_chart(self):
        fig = self.create_chart()
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.get_tk_widget().bind("<Configure>", lambda event: canvas.draw())
        fig.canvas.mpl_connect('button_press_event', functools.partial(on_click, fig, self.title))
        canvas.get_tk_widget().bind("<Enter>", functools.partial(on_enter, fig, canvas))
        canvas.get_tk_widget().bind("<Leave>", functools.partial(on_leave, fig, canvas))
        canvas.draw()

    # Sends the title and percentage to the progress bar creator
    # Makes a canvas on the current frame ID
    # Assigns usage of on_click and mouseover functions
    # Then draws the canvas
    def initiate_progress_bar(self):
        fig = self.create_chart()
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.get_tk_widget().bind("<Configure>", lambda event: canvas.draw())
        fig.canvas.mpl_connect('button_press_event', functools.partial(on_click, fig, self.title))
        canvas.get_tk_widget().bind("<Enter>", functools.partial(on_enter, fig, canvas))
        canvas.get_tk_widget().bind("<Leave>", functools.partial(on_leave, fig, canvas))
        canvas.draw()


class CreateGUI:
    def __init__(self, steamid):
        self.steamid = steamid
        self.gui()

    def test_command(self):
        print('howdy')
        return

    # Makes the root gui frames, top bar with title, profile button, friends list and under frame
    def gui(self):
        root.title("Steam dashboard")
        root.configure(bg=background_colour)
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
        profile_bar = tk.Frame(root, bg=background_colour)
        profile_bar.grid(row=1, column=0, columnspan=1, rowspan=6, sticky="news")

        profile_button = tk.Button(profile_bar, text="Profile", font=(general_font, 16), fg=text_colour,
                                   bg=figure_colour, anchor=tk.CENTER, command=show_profile, height=4)
        profile_button.grid(sticky="news", padx=10, pady=10)
        profile_button.config(width=int(screen_width / 85.3))

        # FRIENDS LIST
        listbox_frame = tk.Frame(root, bg=background_colour)
        listbox_frame.grid(row=3, column=0, rowspan=3, sticky='news')

        self.friends_list = tk.Listbox(listbox_frame, bg=figure_colour, fg=text_colour, selectmode='single', font=(general_font, 17), selectbackground=highlight_colour)
        self.friends_list.config(highlightthickness=0)
        self.friends_list.pack(side='left', fill='y', expand=True)
        find_friends(self.friends_list)

        # BOTTOM FRAME
        bottom_frame = tk.Frame(root, bg=background_colour,)
        bottom_frame.grid(row=4, column=1, columnspan=3, sticky='news')

        under_text = tk.Label(bottom_frame, text='hello there', bg=background_colour, fg=text_colour, font=(general_font, 20))
        under_text.pack(side='left')

        # LOGOUT BUTTON

        logout_bar = tk.Frame(root, bg=background_colour)
        logout_bar.grid(row=4, column=0, columnspan=1, rowspan=6, sticky="news")

        logout_button = tk.Button(logout_bar, text="Logout", font=(general_font, 16), fg=text_colour, bg=figure_colour,
                                  anchor=tk.CENTER, command=show_profile, height=1)
        logout_button.grid(sticky="news", padx=10, pady=10)
        logout_button.config(width=int(screen_width / 85.3))

        self.frames()

    # Graph frames are created and data sent to the initiators
    def frames(self):
        # IMPORTS
        xaxis_2weeks = []
        yaxis_2weeks = []
        used_games = []
        recent_playtime = Ai.games2Weeks(user_id)
        for i in recent_playtime:
            xaxis_2weeks.append(recent_playtime[i]['name'])
            yaxis_2weeks.append(recent_playtime[i]['playtime_2weeks'])
            used_games.append(i)
        achievements = Ai.allAchievements(user_id, used_games[0])
        recent_achievements = Ai.recentGamesAchievements(user_id, used_games[0])
        ach_percentage = achievements['achprocent']

        # FRAME 1
        frame1 = tk.Frame(root)
        frame1.grid(row=2, column=1, padx=graph_frame_padx, pady=graph_frame_pady)
        CreateCharts("pie chart demo 1", yaxis_2weeks, xaxis_2weeks, 'pie', frame1, self.steamid)

        # FRAME 2
        frame2 = tk.Frame(root)
        frame2.grid(row=2, column=2, padx=graph_frame_padx, pady=graph_frame_pady)
        CreateCharts("Your recent playtime (minutes)", yaxis_2weeks, xaxis_2weeks, 'bar', frame2, self.steamid)

        # FRAME 3
        frame3 = tk.Frame(root)
        frame3.grid(row=2, column=3, padx=graph_frame_padx, pady=graph_frame_pady)
        CreateCharts("bar chart demo 2", yaxis_2weeks, xaxis_2weeks, 'bar', frame3, self.steamid)

        # FRAME 4
        frame4 = tk.Frame(root)
        frame4.grid(row=3, column=1, padx=graph_frame_padx, pady=graph_frame_pady)
        CreateCharts("pie chart demo 2", yaxis_2weeks, xaxis_2weeks, 'pie', frame4, self.steamid)

        # FRAME 5
        frame5 = tk.Frame(root)
        frame5.grid(row=3, column=2, padx=graph_frame_padx, pady=graph_frame_pady)
        CreateCharts("achievement % for" + xaxis_2weeks[0], yaxis_2weeks, xaxis_2weeks, 'bar', frame5, self.steamid)

        # FRAME 6

        frame6 = tk.Frame(root)
        frame6.grid(row=3, column=3, padx=graph_frame_padx, pady=graph_frame_pady)
        CreateCharts("achievement % for " + xaxis_2weeks[0], ach_percentage, '0', 'progress', frame6, self.steamid)


class Login:
    def __init__(self):
        self.login_screen = tk.Toplevel(root)
        self.login_screen.configure(bg=background_colour, width=screen_width, height=screen_height)
        self.login_screen.title('Login')

        self.welcome_label = tk.Label(self.login_screen, text="Please enter your login details", font=(general_font, 14), fg=text_colour, bg=background_colour)
        self.welcome_label.grid(row=0, column=0, columnspan=3, sticky="wsne")
        self.welcome_label.grid_columnconfigure(2, weight=1)

        self. username_label = tk.Label(self.login_screen, text="SteamID:", font=(general_font, 14), fg=text_colour, bg=background_colour)
        self.username_label.grid(row=1, column=0, pady=10, padx=10)

        self.login_box = tk.Entry(self.login_screen)
        self.login_box.insert(0, '76561198282499475')
        self.login_box.grid(row=1, column=1, pady=10, padx=10)

        self.login_button = tk.Button(self.login_screen, text='Log me the fuck in', command=self.start_login)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.login_label = tk.Label(self.login_screen, text='', font=(general_font, 14), fg=text_colour, bg=background_colour)
        self.login_label.grid(row=4, column=0, columnspan=2)

        root.withdraw()

    def start_login(self):
        global user_id
        user_id = self.login_box.get()
        if len(user_id) != 17:
            self.login_label.config(text="Invalid steam id")
            raise ValueError('Invalid steam id')
        else:
            self.login_screen.destroy()
            root.deiconify()
            CreateGUI(user_id)



Login()
root.mainloop()
