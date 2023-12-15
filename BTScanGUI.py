import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread
import time
from random import randint

class ctkApp:
    def __init__(self):
        global x
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.root.geometry("1200x400+200x200")
        self.root.title("Dynamic Scatterplot")
        self.UPDATE = True
        self.GRAPH = 'bar'
        self.COLOURS = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']

        self.root.update()

        # Plot frame
        self.frame = ctk.CTkFrame(master=self.root,
                                  height=int(self.root.winfo_height() * 0.95),
                                  width=int(self.root.winfo_width() * 0.66),
                                  fg_color="darkblue")

        self.frame.place(relx=0.33, rely=0.025)

        # Put the plot in
        self.fig, self.ax = plt.subplots()
        #self.fig.set_size_inches(7.5, 3.5)
        self.ax.set(ylim=(0, 70))
        self.ax.bar(x.keys(), height=[i[0] for i in x.values()], label=x.keys(), color=self.COLOURS)
        #self.ax.axis("off")
        #self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.33, rely=0.025)

        # Add buttons
        # Scan on/off button
        scan_button = ctk.CTkButton(master=self.root,
                               width=300,
                               height=50,
                               text="Scan On/Off",
                               command=self.update_on_off)

        scan_button.place(relx=0.025, rely=0.025)

        # Hist button
        hist_button = ctk.CTkButton(master=self.root,
                               width=300,
                               height=50,
                               text="RF1",
                               command=self.swap_graph)

        hist_button.place(relx=0.025, rely=0.35)

        # Quit Button
        quit_button = ctk.CTkButton(master=self.root,
                               width=300,
                               height=50,
                               text="Quit",
                               command=self.quit)

        quit_button.place(relx=0.025, rely=0.85)


    def run(self):
        # Loop

        self.update_window()
        self.root.mainloop()

    def update_window(self):
        # Plot and show the data
        if self.UPDATE:

            if self.GRAPH == 'bar':
                print(x)
                avs = []

                for i in x.values():
                    total = 0
                    for j in i:
                        total += j

                    avs.append(total/len(i))

                self.ax.bar(x.keys(), height=avs, label=x.keys(), color=self.COLOURS)
                self.canvas.draw()
                self.ax.clear()
                self.ax.set(ylim=(0, 70))

            elif self.GRAPH == 'hist':
                self.ax.hist(x['RF1'], bins=30, lw=1, ec="yellow", fc="green", alpha=0.5)
                self.ax.set(ylim=(0, 10))
                self.canvas.draw()
                self.ax.clear()

        self.root.update()
        self.root.after(100, self.update_window)

    def update_on_off(self):
        if self.UPDATE:
            self.UPDATE = False
        else:
            self.UPDATE = True

    def swap_graph(self):
        if self.GRAPH == "bar":
            plt.close()

            self.fig, self.ax = plt.subplots()
            self.ax.hist(x['RF1'], bins=30, lw=1, ec="yellow", fc="green", alpha=0.5)
            self.ax.set(ylim=(0, 10))
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
            self.canvas.draw()
            self.canvas.get_tk_widget().place(relx=0.33, rely=0.025)


            self.GRAPH = 'hist'
        else:
            self.GRAPH = 'bar'

    def quit(self):
        self.root.quit()
        self.root.destroy()


x = {
    "RF1": [40],
    "RF2": [52],
    "RF3": [63],
    "RF4": [34]
}
colours = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']

def generate_RF(x, n=1):
    # Generate n points of RF data
    while True:
        for i in range(n):
            for key in x.keys():
                x[key].append(randint(20, 65))
                if len(x[key]) > 100:
                    x[key].pop(0)
            time.sleep(0.2)


if __name__ == "__main__":
    CTK_Window = ctkApp()

    data = Thread(target=generate_RF, args=(x, 1), daemon=True)

    data.start()
    CTK_Window.run()
    plt.close()


