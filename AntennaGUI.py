import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

class AntennaGUI:
    def __init__(self, root, x, **callbacks):
        self.root = root
        self.UPDATE = True
        self.COLOURS = ["#e50494", "#f77aff", "#7789e1", "#007bc9", "#9dead0",
                        "#7de1ac", "#03b751", "#e9f947", "#cdc90f", "#c5a709"]
        self.create_antenna_hud(x, **callbacks)

    def create_antenna_hud(self, x, **callbacks):
        # Put the plot in
        self.create_av_bar(x, new=True)
        self.create_hist(x)
        self.create_update_bar(x)

        # Add buttons
        # Scan on/off button
        scan_button = ctk.CTkButton(
            master=self.root,
            width=150,
            height=50,
            text="Scan On/Off",
            command=callbacks['toggle_update'])

        scan_button.place(relx=0.020, rely=0.02)

        # Hist button
        hist_button = ctk.CTkButton(
            master=self.root,
            width=150,
            height=50,
            text="View: Antenna",
            command=callbacks['toggle_view'])

        hist_button.place(relx=0.02, rely=0.1)

        # Quit Button
        quit_button = ctk.CTkButton(
            master=self.root,
            width=150,
            height=50,
            text="Quit",
            command=callbacks['quit'])

        quit_button.place(relx=0.02, rely=0.18)

        # Total Signal count textbox
        self.total_device_count = ctk.CTkLabel(
            master=self.root,
            text=f"Total Device Count\n{len(x.MACID.unique())}",
            width=200,
            height=100,
            font=("Roboto",18)
        )
        self.total_device_count.place(relx=0.2, rely=0.02)

        # Active Signal count textbox
        self.total_signal_count = ctk.CTkLabel(
            master=self.root,
            text=f"Total Signal Count\n{x.shape[0]}",
            width=200,
            height=100,
            font=("Roboto",18)
        )
        self.total_signal_count.place(relx=0.2, rely=0.1)

        # Average Signal Strength
        self.av_rssi = ctk.CTkLabel(
            master=self.root,
            text=f"Av. RSSI\n{round(x.RSSI.mean(), 1)}",
            width=200,
            height=100,
            font=("Roboto",18))
        self.av_rssi.place(relx=0.2, rely=0.18)

        # Average Signal Strength
        self.av_signals = ctk.CTkLabel(
            master=self.root,
            text=f"Av. Signals per Second\n{round(x[(x.Time - time.time()) < 5].shape[0], 1)}",
            width=200,
            height=100,
            font=("Roboto",18))
        self.av_signals.place(relx=0.19, rely=0.26)

    def update(self, x):
        self.total_device_count.configure(text=f"Total Device Count\n{len(x.MACID.unique())}")
        self.total_signal_count.configure(text=f"Total Signal Count\n{x.shape[0]}")

        cutoff = 5

        av_rssi = round(x.RSSI[(time.time() - x.Time) < cutoff].mean(), 1)
        av_sig = round(x[(time.time() - x.Time) < cutoff].shape[0] / 5, 1)
        self.av_rssi.configure(text=f"Average RSSI\n{av_rssi}")
        self.av_signals.configure(text=f"Average Signals per Second\n{av_sig}")

        self.create_hist(x, new=False)
        self.create_av_bar(x, new=False)
        self.create_update_bar(x, new=False)

    def create_av_bar(self, x, new=True):
        '''
        Creates or updates a bar graph of average RSSI values
        '''
        plt.close()

        avs = x.groupby('MACID').mean().sort_values(by="RSSI", ascending=False)
        avs = avs.iloc[0:15, :]

        if new:
            self.fig, self.ax = plt.subplots()
            plt.subplots_adjust(bottom=0.35)
            self.fig.set_size_inches(5.75, 4.5)
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)

        self.ax.bar(avs.index, height=avs.RSSI, label=avs.index, color=self.COLOURS)
        self.ax.set(ylim=(0, -120))
        self.ax.set_title('Average RSSI Values')
        self.ax.set_xticklabels(avs.index, rotation=90, fontsize=10)

        self.canvas.draw()

        if new:
            self.canvas.get_tk_widget().place(relx=0.02, rely=0.48)
        else:
            self.ax.clear()

    def create_update_bar(self, x, new=True):
        '''
        Creates or updates a bar graph of average signals received per second over the last 5 seconds
        '''
        plt.close()
        now = time.time()
        counts = x[(now - x.Time) < 5]
        counts = counts.groupby('MACID').count()
        counts.RSSI = counts.RSSI/5
        counts = counts.iloc[0:8, :]
        counts = counts.sort_values(by="RSSI", ascending=False)

        if new:
            self.figup, self.axup = plt.subplots()
            plt.subplots_adjust(bottom=0.35)
            self.figup.set_size_inches(5.75, 4.5)
            self.canvasup = FigureCanvasTkAgg(self.figup, master=self.root)

        self.axup.bar(counts.index, height=counts.RSSI, label=counts.index, color=self.COLOURS)
        self.axup.set_title('Av. Signals per Second')
        self.axup.set_xticklabels(counts.index, rotation=90, fontsize=10)

        self.canvasup.draw()

        if new:
            self.canvasup.get_tk_widget().place(relx=0.5, rely=0.48)
        else:
            self.axup.clear()

    def create_hist(self, x, new=True):
        if new:
            self.figh, self.axh = plt.subplots()
            self.figh.set_size_inches(6.95, 4)
            self.canvash = FigureCanvasTkAgg(self.figh, master=self.root)

        self.axh.hist(x.RSSI, bins=12, lw=1, ec="yellow", fc="green", alpha=0.5)
        self.canvash.draw()

        if new:
            self.canvash.get_tk_widget().place(relx=0.4, rely=0.025)
        else:
            self.axh.clear()

    def destroy(self):
        plt.close('all')

        for widget in self.root.winfo_children():
            widget.destroy()
