# import all bullshit
import functools
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
import tkinter as tk
from datetime import datetime
from time import strftime
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from AI import Ai
from TI import ti
import keyboard


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
def on_click(fig, title, frame, event):
    Details(frame, title)


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
    sorted_friends = Ai.sortedFriends(user_id, 0)
    for i in sorted_friends:
        friends_list.insert(tk.END, i)
    return


# hides the root window and opens the login window
def logout_function():
    for widget in root.winfo_children():
        widget.destroy()
    Login()
    return


def private_checker(steamid):
    return Ai.privateChecker(steamid)


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
        plt.style.use('dark_background')
        if self.chart_type == "infomenu":
            new_data = {'time': [], 'name': []}
            for content in self.data.values():
                for data in content:
                    if type(data) == int:
                        new_data['time'].append(datetime.utcfromtimestamp(data).strftime('%Y-%m-%d'))
                    else:
                        new_data['name'].append(data)
            content = pd.DataFrame(new_data, columns=None)
            fig.text(0.5, 0.8, 'Recent achievements', fontsize=30, horizontalalignment='center')
            fig.text(0.5, 0.7, self.title, fontsize=20, horizontalalignment='center')
            fig.text(0.5, 0.4, content.to_string(index=False, header=False), fontsize=12, horizontalalignment='center')
            return fig
        elif self.chart_type == "welcome":
            fig.text(0.5, 0.7, self.title, fontsize=20, horizontalalignment='center')
            fig.text(0.5, 0.4, 'hi there', fontsize=12, horizontalalignment='center')
            return fig
        elif self.chart_type == 'clock':
            string = strftime('%d/%m/%Y')
            fig.text(0.5, 0.7, self.title, fontsize=30, horizontalalignment='center')
            fig.text(0.5, 0.5, "today's date:", fontsize=20, horizontalalignment='center')
            fig.text(0.5, 0.4, string, fontsize=20, horizontalalignment='center')
            return fig
        elif self.chart_type == "void":
            plt.style.use('dark_background')
            if self.data == -1:
                fig.text(0.5, 0.8, 'Recent playtime (minutes)', fontsize=20, horizontalalignment='center')
            elif self.data == -2:
                fig.text(0.5, 0.8, 'Recent achievements', fontsize=30, horizontalalignment='center')
            fig.text(0.5, 0.5, self.title, fontsize=14, horizontalalignment='center')
            return fig
        else:
            if self.chart_type == "progress":
                ax = fig.add_subplot(513)
                self.title = f"Achievement % for {self.title}"
            else:
                ax = fig.add_subplot(111)
            ax.set_facecolor(backboard_colour)
            ax.set_title(self.title, fontsize=20)
            if self.chart_type == "bar":
                bars = ax.barh(self.axis, self.data)
                ax.bar_label(bars)
            elif self.chart_type == "progress":
                ax.set_xlim([0, 100])
                ax.set_yticks([])
                rect = plt.Rectangle((0, 0), self.data, 1, color=highlight_colour)
                ax.add_patch(rect)
            elif self.chart_type == "pie":
                ax.pie(self.data, labels=self.axis, colors=['#1b2838', 'black', '#c7d5e0', '#66c0f4', '#171a21'])
            else:
                raise ValueError("Invalid chart type")
        return fig

    # Sends the title, plot data and axis titles to the pie chart creator
    # Makes a canvas on the current frame ID
    # Assigns usage of on_click and mouseover functions
    # Then draws the canvas
    def initiate_chart(self):
        if not self.steamId == user_id:
            self.friendname = friends_dict[f'{self.steamId}']['name']
        else:
            self.friendname = user_name
        if self.data == -1:
            self.title = f'{self.friendname} has touched grass'
            self.chart_type = 'void'
        elif self.data == -2:
            self.title = f'{self.friendname} has not gotten any achievements\nin the past 2 weeks for {self.title}'
            self.chart_type = 'void'
        elif self.data == -3:
            self.title = f'Welcome'
        fig = self.create_chart()
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.get_tk_widget().bind("<Configure>", lambda event: canvas.draw())
        fig.canvas.mpl_connect('button_press_event', functools.partial(on_click, fig, self.title, self.frame))
        canvas.get_tk_widget().bind("<Enter>", functools.partial(on_enter, fig, canvas))
        canvas.get_tk_widget().bind("<Leave>", functools.partial(on_leave, fig, canvas))
        canvas.draw()


class CreateGUI:

    def __init__(self, steamid):
        self.steamid = steamid
        self.index = 10
        self.gui()


    # when clicking a friend in the friends list
    # this function determines who you clicked on and checks if their profile is private using a function in Ai.py
    # calls either the refresh_data function or the profile_error function
    def list_select(self, event):
        self.picked = event.widget.get(self.selection)
        self.ID = flipped_friends_dict[self.picked]['id']
        private = private_checker(self.ID)
        if private['games']:
            self.profile_error()
        else:
            self.refresh_data()

    def on_list_click(self, event):
        self.selection = event.widget.curselection()[0]
        self.list_select(event)

    def keypress_down(self, event):
        self.friends_list.select_clear(self.selection)
        self.selection += 1
        self.friends_list.select_set(self.selection)
        self.list_select(event)
        self.refocus()

    def keypress_up(self, event):
        self.friends_list.select_clear(self.selection)
        self.selection -= 1
        self.friends_list.select_set(self.selection)
        self.list_select(event)
        self.refocus()

    def refocus(self):
        root.after(50, self.friends_list.focus_force())

    def show_profile(self):
        self.ID = user_id
        self.refresh_data()
        return

    def refresh_data(self):
        self.frame2.destroy()
        self.frame3.destroy()
        self.frame5.destroy()
        self.frame6.destroy()
        self.steamid = self.ID
        self.data(self.steamid)
        self.frames()

    def start_ti(self):
        input = ti.start().strip()
        if input == str(0):
            keyboard.press_and_release('Up')
        elif input == str(1):
            keyboard.press_and_release('Down')

    def profile_error(self):
        self.private_error = tk.Toplevel(root)
        self.private_error.geometry(f'{popup_window_width}x{popup_window_height}+{int(popup_x)}+{int(popup_y)}')
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

        sensor_button = tk.Button(profile_bar, text="Sensor on", font=(general_font, 16), fg=text_colour,
                                   bg=figure_colour, anchor=tk.CENTER, command=self.start_ti, height=1)
        sensor_button.grid(sticky="news", padx=10, pady=10)
        sensor_button.config(width=int(screen_width / 85.3))

        # FRIENDS LIST
        self.listbox_frame = tk.Frame(root, bg=background_colour)
        self.listbox_frame.grid(row=2, column=0, rowspan=3, sticky='news')

        self.friends_list = tk.Listbox(self.listbox_frame, bg=figure_colour, fg=text_colour, selectmode='single',\
                                  font=(general_font, 17), selectbackground=highlight_colour)
        self.friends_list.config(highlightthickness=0)
        self.friends_list.bind("<<ListboxSelect>>", self.on_list_click)
        self.friends_list.bind("<KeyRelease-Down>", self.keypress_down)
        self.friends_list.bind("<KeyRelease-Up>", self.keypress_up)
        self.friends_list.pack(side='left', fill='y', expand=True)
        find_friends(self.friends_list)
        self.selection = 0
        self.friends_list.select_set(self.selection)


        # BOTTOM FRAME
        bottom_frame = tk.Frame(root, bg=background_colour,)
        bottom_frame.grid(row=4, column=1, columnspan=3, sticky='news')

        under_text = tk.Label(bottom_frame, text='hello there', bg=background_colour, fg=text_colour, font=(general_font, 20))
        under_text.pack(side='left')

        # LOGOUT BUTTON
        logout_bar = tk.Frame(root, bg=background_colour)
        logout_bar.grid(row=4, column=0, columnspan=1, rowspan=6, sticky="news")

        logout_button = tk.Button(logout_bar, text="Logout", font=(general_font, 16), fg=text_colour, bg=figure_colour,
                                  anchor=tk.CENTER, command=Login, height=1)
        # EDIT BACK LATER TO LOGOUT
        logout_button.grid(sticky="news", padx=10, pady=10)
        logout_button.config(width=int(screen_width / 85.3))

        self.statics()
        self.data(user_id)
        self.frames()
        self.refocus()


    def statics(self):
        # clock
        self.frame1 = tk.Frame(root)
        self.frame1.grid(row=2, column=1, padx=graph_frame_padx, pady=graph_frame_pady)
        CreateCharts("", -3, '', 'clock', self.frame1, self.steamid)

        self.xaxis_freq = []
        self.yaxis_freq = []
        self.frequency = Ai.frequencyGamesAllFriends(self.steamid)
        for i in range(5):
            self.xaxis_freq.append(self.frequency['name'][i])
            self.yaxis_freq.append(self.frequency['frequency'][i])
        # FRAME 4
        self.frame4 = tk.Frame(root)
        self.frame4.grid(row=3, column=1, padx=graph_frame_padx, pady=graph_frame_pady)
        CreateCharts("Your friends are playing", self.yaxis_freq, self.xaxis_freq, 'bar', self.frame4, self.steamid)

    def data(self, steamid):
        # Declare recent playtime
        self.xaxis_2weeks = []
        self.yaxis_2weeks = []
        self.used_games = []
        self.mostplayed = []
        self.recent_playtime = Ai.games2Weeks(steamid)
        if not self.recent_playtime:
            self.xaxis_2weeks = -1
            self.yaxis_2weeks = -1
            self.gamename = ''
        else:
            for game in self.recent_playtime:
                self.xaxis_2weeks.append(self.recent_playtime[game]['name'])
                self.yaxis_2weeks.append(self.recent_playtime[game]['playtime_2weeks'])
                self.used_games.append(game)
                self.gamename = self.xaxis_2weeks[0]
                self.mostplayed = self.used_games[0]
        # Declare achievement stats
        self.achievements = {}
        self.achievements = Ai.allAchievements(steamid, self.mostplayed)
        if not self.achievements:
            self.ach_percentage = -2
            self.achievement_stats = -2
        else:
            self.achievement_stats = Ai.recentGamesAchievements(steamid, self.mostplayed)
            self.ach_percentage = self.achievements['achprocent']


    # Graph frames are created and data sent to the initiators
    def frames(self):

        # FRAME 2
        self.frame2 = tk.Frame(root)
        self.frame2.grid(row=2, column=2, padx=graph_frame_padx, pady=graph_frame_pady)
        CreateCharts("Recent playtime (minutes)", self.yaxis_2weeks, self.xaxis_2weeks, 'bar', self.frame2, self.steamid)

        # FRAME 3
        self.frame3 = tk.Frame(root)
        self.frame3.grid(row=2, column=3, padx=graph_frame_padx, pady=graph_frame_pady)
        CreateCharts(f"{self.gamename}", self.achievement_stats, '0', 'infomenu', self.frame3, self.steamid)

        # FRAME 5
        self.frame5 = tk.Frame(root)
        self.frame5.grid(row=3, column=2, padx=graph_frame_padx, pady=graph_frame_pady)
        CreateCharts("Recent playtime (minutes)", self.yaxis_2weeks, self.xaxis_2weeks, 'pie', self.frame5, self.steamid)

        # FRAME 6
        self.frame6 = tk.Frame(root)
        self.frame6.grid(row=3, column=3, padx=graph_frame_padx, pady=graph_frame_pady)
        CreateCharts(self.gamename, self.ach_percentage, '0', 'progress', self.frame6, self.steamid)




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
        self.login_box.insert(0, '76561198282499475')
        self.login_box.pack(expand=True)

        self.login_button = tk.Button(self.login_screen, text='Login', command=self.start_login, font=28)
        self.login_button.pack(expand=True)

        self.login_label = tk.Label(self.login_screen, text='', font=(general_font, 28), fg=text_colour, bg=background_colour)
        self.login_label.pack(expand=True)

        root.withdraw()

    def start_login(self):
        global user_id
        user_id = self.login_box.get()
        global user_name
        user_name = Ai.personalData(user_id)['name']
        private = private_checker(user_id)
        if private is None:
            self.login_label.config(text="Invalid steam id")
            raise ValueError('Invalid steam id')
        elif private['friends'] or private['games']:
            CreateGUI.profile_error(CreateGUI)
        else:
            self.login_screen.destroy()
            root.deiconify()
            CreateGUI(user_id)


class Details:
    def __init__(self, frame, title):
        self.title = title
        self.frame = frame
        self.details_window = tk.Toplevel(root)
        self.details_window.geometry(f'{popup_window_width}x{popup_window_height}+{int(popup_x)}+{int(popup_y)}')
        self.details_window.configure(bg=background_colour, width=screen_width, height=screen_height)
        self.details_window.title('Details')
        self.details_window.grab_set()
        self.details_build()

    def details_build(self):

        if str(self.title) == 'Welcome':
            frame_title = 'Welcome'
            info = "This is simply a welcome,\n I don't know what you expected"
        elif str(self.title) == 'Recent playtime (minutes)':
            frame_title = 'Recent playtime'
            info = 'Here you see how many \nminutes you or your friend has played their \nmost recent games in the past 2 weeks'
        elif str(self.title) == '.!frame9':
            frame_title = ''
            info = ''
        elif str(self.title) == '.!frame10':
            frame_title = ''
            info = ''
        else:
            frame_title = 'Achievements'
            info = 'An overview of \nunlocked achievements for your most \nplayed game in the past 2 weeks'

        self.return_button = tk.Button(self.details_window, text='return', font=(general_font, 16), fg=text_colour,
                                       bg=figure_colour, anchor=tk.CENTER, command=self.details_return, height=2)
        self.return_button.config(width=int(screen_width / 85.3))
        self.return_button.pack(side=tk.BOTTOM, pady=10)

        self.label = tk.Label(self.details_window, text=info, bg=background_colour, fg=text_colour, font=(general_font, 18))
        self.label.pack(side=tk.BOTTOM, pady=10)

        self.title_label = tk.Label(self.details_window, text=frame_title, bg=background_colour, fg=text_colour, font=(general_font, 26))
        self.title_label.pack(side=tk.BOTTOM, pady=10)
    def details_return(self):
        self.details_window.destroy()


if __name__ == '__main__':
    Login()
    root.mainloop()



