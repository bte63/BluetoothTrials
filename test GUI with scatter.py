import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
from threading import Thread
import time

class ctkApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.root.geometry("1200x400+200x200")
        self.root.title("Dynamic Scatterplot")
        self.UPDATE = True

        self.root.update()

        # Plot frame
        self.frame = ctk.CTkFrame(master=self.root,
                                  height=int(self.root.winfo_height() * 0.95),
                                  width=int(self.root.winfo_width() * 0.66),
                                  fg_color="darkblue")

        self.frame.place(relx=0.33, rely=0.025)

        # Put the plot in
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(7.5, 3.5)
        self.ax.scatter(x, y, 1.5, color='black', alpha=0.3)
        self.ax.axis("off")
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.33, rely=0.025)

        # Add buttons
        # Scan on/off button
        Button1 = ctk.CTkButton(master=self.root,
                               width=300,
                               height=50,
                               text="Scan On/Off",
                               command=self.update_on_off)

        Button1.place(relx=0.025, rely=0.025)

        # Quit Button
        Button2 = ctk.CTkButton(master=self.root,
                               width=300,
                               height=50,
                               text="Quit",
                               command=self.quit)

        Button2.place(relx=0.025, rely=0.85)


    def run(self):
        # Loop

        self.update_window()
        self.root.mainloop()

    def update_window(self):
        # Plot and show the data
        if self.UPDATE:
            self.ax.scatter(x, y, 1.5, color='black', alpha=0.3)
            self.canvas.draw()

        self.root.update()
        self.root.after(100, self.update_window)

    def update_on_off(self):
        if self.UPDATE:
            self.UPDATE = False
        else:
            self.UPDATE = True

    def quit(self):
        self.root.quit()
        self.root.destroy()



global x, y, z
x = [0.2]
y = [1.2]
z = [0.8]

def generate_SA(x, y, z, n=100):
    # Generate n points of strange attractor data
    while True:
        for i in range(n):
            new_x = x[-1] + math.sin(y[-1]) - 0.208186 * x[-1]
            new_y = y[-1] + math.sin(z[-1]) - 0.208186 * y[-1]
            new_z = z[-1] + math.sin(x[-1]) - 0.208186 * z[-1]

            x.append(new_x)
            y.append(new_y)
            z.append(new_z)

            time.sleep(0.02)


if __name__ == "__main__":
    CTK_Window = ctkApp()

    data = Thread(target=generate_SA, args=[x, y, z, 200], daemon=True)

    data.start()
    CTK_Window.run()
    plt.close()


