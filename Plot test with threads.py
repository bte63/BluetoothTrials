import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
from threading import Thread

global x, y, z
x = [0.2]
y = [1.2]
z = [0.8]

def generate_SA(n, x, y, z):
    # Generate n points of strange atttractor data
    for i in range(n):
        new_x = x[-1] + math.sin(y[-1]) - 0.208186 * x[-1]
        new_y = y[-1] + math.sin(z[-1]) - 0.208186 * y[-1]
        new_z = z[-1] + math.sin(x[-1]) - 0.208186 * z[-1]

        x.append(new_x)
        y.append(new_y)
        z.append(new_z)


class ctkApp:

    def __init__(self):
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.root.geometry("1200x400+200x200")
        self.root.title("Dynamic Scatterplot")
        self.root.update()

        # Plot frame
        self.frame = ctk.CTkFrame(master=self.root,
                                  height=self.root.winfo_height() * 0.95,
                                  width=self.root.winfo_width() * 0.66,
                                  fg_color="darkblue")

        self.frame.place(relx=0.33, rely=0.025)

        # Put the plot in
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(11, 5.3)
        self.ax.scatter(x, y, 1.5, color='black', alpha=0.3)
        self.ax.axis("off")
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.33, rely=0.025)


    def run(self):
        # Loop
        self.update_window()
        self.root.mainloop()

    def update_window(self):
        # Generate new data
        #self.update_data()

        # Plot and show the data
        self.ax.scatter(x, y, 1.5, color='black', alpha=0.3)
        self.canvas.draw()

        self.root.update()
        self.root.after(100, self.update_window)

    def update_data(self):
        for i in range(1000):
            new_x = x[-1] + math.sin(y[-1]) - 0.208186 * x[-1]
            new_y = y[-1] + math.sin(z[-1]) - 0.208186 * y[-1]
            new_z = z[-1] + math.sin(x[-1]) - 0.208186 * z[-1]

            x.append(new_x)
            y.append(new_y)
            z.append(new_z)



if __name__ == "__main__":
    CTK_Window = ctkApp()

    gui = Thre

    plt.close()



fr



