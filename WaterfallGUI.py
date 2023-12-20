import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import numpy as np
import pandas as pd

class WaterfallGUI:
    def __init__(self, root, x, **callbacks):
        self.root = root
        self.UPDATE = True
        self.update_counter = 1
        self.WATERFALL_LENGTH = 100
        self.Y_AXIS = np.arange(self.WATERFALL_LENGTH)
        self.sample_macs(x)

        self.create_waterfall_hud(x, **callbacks)

    def sample_macs(self, x):
        self.MACIDS = x.MACID.unique()
        self.waterfall_container = pd.DataFrame(np.zeros((self.WATERFALL_LENGTH, len(self.MACIDS))))
        self.waterfall_container.columns = self.MACIDS


    def create_waterfall_hud(self, x, **callbacks):
        # Put the plot in
        self.create_waterfall(x, new=True)

        # Quit Button
        quit_button = ctk.CTkButton(
            master=self.root,
            width=150,
            height=50,
            text="Quit",
            command=callbacks['quit'])

        quit_button.place(relx=0.02, rely=0.18)

    def update(self, x):
        if self.update_counter < 10:
            self.sample_macs(x)

        else:
            self.create_waterfall(x, new=False)

        self.update_counter += 1

    def create_waterfall(self, x, new=True):
        if new:
            self.fig, self.ax = plt.subplots()
            self.fig.set_size_inches(11.5, 4.5)
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)

        now = x.Time.max()

        # Subset the data
        data = x[x.Time >= now - 1]

        # Clean the time column
        data.loc[:, "Time"] = round(now - data.Time, 1)

        grouped_df = data[["MACID", "RSSI"]].groupby(["MACID"])
        grouped_df = grouped_df.mean().T

        # Add it in
        self.waterfall_container = pd.concat([self.waterfall_container, grouped_df], ignore_index=True)
        self.waterfall_container.fillna(0, inplace=True)
        self.waterfall_container = self.waterfall_container.iloc[1:, :]



        # rssi_vals = []
        # # For every MACID in x
        # # We need to (without looping) convert the data into a df with MACID in columns and
        # # RSSI values for each second in rows, then apply some smoothing function
        # for mac in x_axis:
        #     out = []
        #     subset = data[data.MACID==mac]
        #     for second in range(30):
        #         if second in subset.Time.values:
        #             out.append(subset.RSSI[subset.Time == second].mean())
        #         else:
        #             out.append(0)
        #
        #     rssi_vals.append(out)
        #
        # rssi_vals = np.array(rssi_vals)
        # rssi_vals = rssi_vals.T
        # #print(rssi_vals)
        #
        # # if self.update_counter == 50:
        # #     x.to_csv("sample_data.csv", index_label=False)
        #
        # if len(rssi_vals) > 0:
        #     y_axis = np.arange(30)


        self.ax.pcolormesh(self.MACIDS, self.Y_AXIS, self.waterfall_container.T)
        self.canvas.draw()

        if new:
            self.canvas.get_tk_widget().place(relx=0.02, rely=0.48)
        else:
            self.ax.clear()

    def destroy(self):
        plt.close('all')

        for widget in self.root.winfo_children():
            widget.destroy()