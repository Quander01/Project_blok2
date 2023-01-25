# import all bullshit
import functools
import matplotlib
import tkinter as tk
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from AI import Ai
matplotlib.use("TkAgg")


# declares all globals for styling
if __name__ == '__main__':
    root = tk.Tk()
    # screen sizes
    screen_height = int(root.winfo_screenheight()/1.2)
    screen_width = int(root.winfo_screenwidth()/1.2)
    x = (screen_width/10)
    y = (screen_height/10)

    # overlay window sizes
    overlay_window_height = int(screen_height/1.2)
    overlay_window_width = int(screen_width/1.2)
    overlay_x = (screen_width/2) - (overlay_window_width/2.6)
    overlay_y = (screen_width/2) - (overlay_window_height/1.2)

    # popup window sizes
    popup_window_height = int(screen_height/4)
    popup_window_width = int(screen_width/4)
    popup_x = (screen_width/2) - (popup_window_width/8)
    popup_y = (screen_width/2) - (popup_window_height*2)

    # root window configuration
    root.geometry("{}x{}".format(screen_width, screen_height))
    root.geometry(f'{screen_width}x{screen_height}+{int(x)}+{int(y)}')

    # Colour assignments
    text_colour = '#c7d5e0'                                         # slightly blue white-ish
    background_colour = '#1b2838'                                   # steam dark blue
    figure_colour = '#2a475e'                                       # steam blue
    backboard_colour = '#232323'                                    # steam dark grey
    highlight_colour = '#66c0f4'                                    # steam light blue

    # Graph sizes
    graph_frame_padx = screen_width/170.6
    graph_frame_pady = screen_height/96

    # Font management
    general_font = 'Arial'
    plt.rcParams['text.color'] = text_colour
    px = 1/plt.rcParams['figure.dpi']


# Function to open the info windows when clicking on charts
# takes the title of the selected graph
def on_click(fig, title, event):
    print("you clicked on", title)
    Details()


# Register when the cursor enters the chart area and change the colour
def on_enter(fig, canvas, event):
    fig.set_facecolor(highlight_colour)
    canvas.draw()


# Register when the cursor leaves the chart area and change the colour back accordingly
def on_leave(fig, canvas, event):
    fig.set_facecolor(figure_colour)
    canvas.draw()


# Function imports friends from Ai.py based on steamid
# then loops through the returned dictionary to fill the listbox with names
def find_friends(friends_list):
    global friends_dict
    global flipped_friends_dict
    friends_dict = Ai.friendlistData(user_id)
    flipped_friends_dict = Ai.flipIDData(friends_dict)
    for i in friends_dict:
        friends_list.insert(tk.END, friends_dict[i]['name'])
    return


# hides the root window and opens the login window
def logout_function():
    root.withdraw()
    Login()
    return


def private_checker(steamid):
    if Ai.privateChecker(steamid):
        return True
    else:
        return False


def On_entry_up_down(event):
    selection = event.widget.curselection()[0]

    if event.keysym == 'Up':
        selection += -1

    if event.keysym == 'Down':
        selection += 1

    if 0 <= selection < event.widget.size():
        event.widget.selection_clear(0, tk.END)
        event.widget.select_set(selection)

class CreateCharts:
    def __init__(self, title, data, axis, chart_type, frame, steamid):
        self.steamId = steamid
        self.chart_type = chart_type
        self.title = title
        self.axis = axis
        self.data = data
        self.frame = frame
        self.initiate_chart()

    # Function takes in three parameters: title of the figure, axis names and data to display.
    # It creates and returns a pie chart using the matplotlib library.
    def create_chart(self):
        plt.rcParams['text.color'] = text_colour
        fig = Figure(facecolor=figure_colour, figsize=(screen_width / 3.8 * px, screen_height / 2.7 * px))
        if self.chart_type == "infomenu":
            content = pd.DataFrame(self.data)
            fig.text(0.1, 0.5, str(content), fontsize=14)
            return fig
        else:
            if self.chart_type == "progress":
                ax = fig.add_subplot(513)
            else:
                ax = fig.add_subplot(111)
            ax.set_facecolor(backboard_colour)
            ax.set_title(self.title)
            if self.chart_type == "void":
                plt.style.use('dark_background')
            elif self.chart_type == "bar":
                bars = ax.barh(self.axis, self.data)
                ax.bar_label(bars)
            elif self.chart_type == "progress":
                ax.set_xlim([0, 100])
                ax.set_yticks([])
                rect = plt.Rectangle((0, 0), self.data, 1, color=highlight_colour)
                ax.add_patch(rect)
            elif self.chart_type == "pie":
                plt.style.use('dark_background')
                ax.pie(self.data, labels=self.axis, colors=['#1b2838', 'black', '#c7d5e0', '#66c0f4', '#171a21'])
            else:
                raise ValueError("Invalid chart type")
        return fig

    # Sends the title, plot data and axis titles to the pie chart creator
    # Makes a canvas on the current frame ID
    # Assigns usage of on_click and mouseover functions
    # Then draws the canvas
    def initiate_chart(self):
        if self.data == -1:
            print("nah fam, graphie gaat niet gemaakt worden")
            self.title = 'Er zijn geen achievements gevonden voor \n je meest gespeelde spel in de afgelopen 2 weken'
            self.chart_type = 'void'
            fig = self.create_chart()
            canvas = FigureCanvasTkAgg(fig, master=self.frame)
            canvas.draw()
            return
        else:
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
        #print(Ai.frequencyGamesAllFriends(self.steamid))
        self.gui()

    # when clicking a friend in the friends list
    # this function determines who you clicked on and checks if their profile is private using a function in Ai.py
    # calls either the refresh_data function or the profile_error function
    def list_select(self, event):
        selection = event.widget.curselection()
        picked = event.widget.get(selection[0])
        self.ID = flipped_friends_dict[picked]['id']
        if private_checker(self.ID):
            self.profile_error()
        else:
            self.refresh_data()

    def show_profile(self):
        self.ID = user_id
        self.refresh_data()
        return

    def refresh_data(self):
        self.frame1.destroy()
        self.frame2.destroy()
        self.frame3.destroy()
        self.frame4.destroy()
        self.frame5.destroy()
        self.frame6.destroy()
        self.steamid = self.ID
        self.frames(self.steamid)

    def profile_error(self):
        self.private_error = tk.Toplevel(root)
        self.private_error.geometry(f'{overlay_window_width}x{overlay_window_height}+{int(overlay_x)}+{int(overlay_y)}')
        self.private_error.configure(bg=background_colour, width=overlay_window_width, height=overlay_window_height)
        self.private_error.title('error')
        self.private_error.grab_set()

        self.error_label = tk.Label(self.private_error, text="This profile is private",
                                    font=(general_font, 30), fg=text_colour, bg=background_colour, pady=20)
        self.error_label.pack()

        self.ok_button = tk.Button(self.private_error, text='OK', font=(general_font, 20),
                                      command=self.private_error.destroy)
        self.ok_button.pack(expand=True)

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

        title_label = tk.Label(title_bar, text="Steam Dashboard", font=(general_font, 30), fg=text_colour,\
                               bg=backboard_colour, anchor=tk.CENTER)
        title_label.grid(row=0, column=2, pady=screen_height/19.2)

        # PROFILE BUTTON
        profile_bar = tk.Frame(root, bg=background_colour)
        profile_bar.grid(row=0, column=0, columnspan=1, rowspan=6, sticky="news")

        profile_button = tk.Button(profile_bar, text="Back to my data", font=(general_font, 16), fg=text_colour,
                                   bg=figure_colour, anchor=tk.CENTER, command=self.show_profile, height=4)
        profile_button.grid(sticky="news", padx=10, pady=10)
        profile_button.config(width=int(screen_width / 85.3))

        # FRIENDS LIST
        listbox_frame = tk.Frame(root, bg=background_colour)
        listbox_frame.grid(row=2, column=0, rowspan=3, sticky='news')

        friends_list = tk.Listbox(listbox_frame, bg=figure_colour, fg=text_colour, selectmode='single',\
                                  font=(general_font, 17), selectbackground=highlight_colour)
        friends_list.config(highlightthickness=0)
        friends_list.bind("<<ListboxSelect>>", self.list_select)
        friends_list.pack(side='left', fill='y', expand=True)
        find_friends(friends_list)
        friends_list.select_set(0)
        friends_list.bind("<Down>", On_entry_up_down)
        friends_list.bind("<Up>", On_entry_up_down)

        # BOTTOM FRAME
        bottom_frame = tk.Frame(root, bg=background_colour,)
        bottom_frame.grid(row=4, column=1, columnspan=3, sticky='news')

        under_text = tk.Label(bottom_frame, text='hello there', bg=background_colour, fg=text_colour, font=(general_font, 20))
        under_text.pack(side='left')

        # LOGOUT BUTTON

        logout_bar = tk.Frame(root, bg=background_colour)
        logout_bar.grid(row=4, column=0, columnspan=1, rowspan=6, sticky="news")

        logout_button = tk.Button(logout_bar, text="Logout", font=(general_font, 16), fg=text_colour, bg=figure_colour,
                                  anchor=tk.CENTER, command=logout_function, height=1)
        logout_button.grid(sticky="news", padx=10, pady=10)
        logout_button.config(width=int(screen_width / 85.3))

        self.frames(user_id)

    # Graph frames are created and data sent to the initiators
    def frames(self, steamid):
        # IMPORTS
        achievements = []
        xaxis_2weeks = []
        yaxis_2weeks = []
        used_games = []
        recent_playtime = Ai.games2Weeks(steamid)
        if recent_playtime:
            for game in recent_playtime:
                xaxis_2weeks.append(recent_playtime[game]['name'])
                yaxis_2weeks.append(recent_playtime[game]['playtime_2weeks'])
                used_games.append(game)
                achievements = Ai.allAchievements(steamid, used_games[0])
        else:
            raise ValueError('geen data gevonden')

        if achievements == 0:
            ach_percentage = -1
            achievement_stats = Ai.recentGamesAchievements(steamid, used_games[0])
        else:
            achievement_stats = Ai.recentGamesAchievements(steamid, used_games[0])
            print(achievement_stats)
            #for time in achievement_stats:
            #    achievement_stats[time] = (datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'))
            # print(achievement_stats)
            ach_percentage = achievements['achprocent']


        # FRAME 1
        self.frame1 = tk.Frame(root)
        self.frame1.grid(row=2, column=1, padx=graph_frame_padx, pady=graph_frame_pady)
        CreateCharts("Your recent playtime (minutes)", yaxis_2weeks, xaxis_2weeks, 'pie', self.frame1, self.steamid)

        # FRAME 2
        self.frame2 = tk.Frame(root)
        self.frame2.grid(row=2, column=2, padx=graph_frame_padx, pady=graph_frame_pady)
        CreateCharts("Your recent playtime (minutes)", yaxis_2weeks, xaxis_2weeks, 'bar', self.frame2, self.steamid)

        # FRAME 3
        self.frame3 = tk.Frame(root)
        self.frame3.grid(row=2, column=3, padx=graph_frame_padx, pady=graph_frame_pady)
        CreateCharts("achievements?", achievement_stats, '0', 'infomenu', self.frame3, self.steamid)

        # FRAME 4
        self.frame4 = tk.Frame(root)
        self.frame4.grid(row=3, column=1, padx=graph_frame_padx, pady=graph_frame_pady)
        CreateCharts("pie chart demo 2", yaxis_2weeks, xaxis_2weeks, 'pie', self.frame4, self.steamid)

        # FRAME 5
        self.frame5 = tk.Frame(root)
        self.frame5.grid(row=3, column=2, padx=graph_frame_padx, pady=graph_frame_pady)
        CreateCharts("achievement % for" + xaxis_2weeks[0], yaxis_2weeks, xaxis_2weeks, 'bar', self.frame5, self.steamid)

        # FRAME 6
        self.frame6 = tk.Frame(root)
        self.frame6.grid(row=3, column=3, padx=graph_frame_padx, pady=graph_frame_pady)
        CreateCharts("achievement % for " + xaxis_2weeks[0], ach_percentage, '0', 'progress', self.frame6, self.steamid)


class Login:
    def __init__(self):
        self.login_screen = tk.Toplevel(root)
        self.login_screen.configure(bg=background_colour, width=screen_width, height=screen_height)
        self.login_screen.title('Login')
        self.login_screen.geometry(f'{popup_window_width}x{popup_window_height}+{int(popup_x)}+{int(popup_y)}')

        self.welcome_label = tk.Label(self.login_screen, text="Please enter your login details", font=(general_font, 28), fg=text_colour, bg=background_colour)
        self.welcome_label.pack(expand=True)

        self. username_label = tk.Label(self.login_screen, text="SteamID:", font=(general_font, 20), fg=text_colour, bg=background_colour)
        self.username_label.pack(expand=True)

        self.login_box = tk.Entry(self.login_screen, font=28)
        self.login_box.insert(0, '76561198111929702')
        self.login_box.pack(expand=True)

        self.login_button = tk.Button(self.login_screen, text='Login', command=self.start_login, font=28)
        self.login_button.pack(expand=True)

        self.login_label = tk.Label(self.login_screen, text='', font=(general_font, 28), fg=text_colour, bg=background_colour)
        self.login_label.pack(expand=True)

        root.withdraw()

    def start_login(self):
        global user_id
        user_id = self.login_box.get()
        private = private_checker(user_id)
        if private:
            CreateGUI.profile_error(CreateGUI)
        elif private is None:
            self.login_label.config(text="Invalid steam id")
            raise ValueError('Invalid steam id')
        elif not private:
            self.login_screen.destroy()
            root.deiconify()
            CreateGUI(user_id)


class Details:
    def __init__(self):
        self.details_window = tk.Toplevel(root)
        self.details_window.geometry(f'{overlay_window_width}x{overlay_window_height}+{int(overlay_x)}+{int(overlay_y)}')
        self.details_window.configure(bg=background_colour, width=screen_width, height=screen_height)
        self.details_window.title('Details')
        self.details_window.grab_set()

        self.details_label = tk.Label(self.details_window, text='Howdy partner')
        self.details_label.pack()

        self.return_button = tk.Button(self.details_window, text='return', command=self.details_window.destroy)
        self.return_button.pack()


if __name__ == '__main__':
    Login()
    root.mainloop()
