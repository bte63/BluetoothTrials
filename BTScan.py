import time
import pandas as pd
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread
from gi.repository import GLib
from pydbus import SystemBus
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


class ctkApp:
    def __init__(self):
        global x
        self.WIDTH=1200
        self.HEIGHT=900
        self.UPDATE = True
        self.GRAPH = 'bar'
        self.COLOURS = ["#e50494", "#f77aff", "#7789e1", "#007bc9", "#9dead0",
                        "#7de1ac", "#03b751", "#e9f947", "#cdc90f", "#c5a709"]
        self.MAC_IDS = []
        self.QUIT = False

        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.root.geometry("1200x900+200x200")
        self.root.title("BTScan")
        self.root.update()
        self.create_antenna_hud()


    def run(self):
        # Loop

        self.update_window()
        self.root.mainloop()

    def update_window(self):
        # Plot and show the data
        if self.UPDATE:
            if self.GRAPH == 'bar':
                self.create_graph(graph_type='bar', new=False)

            elif self.GRAPH == 'hist':
                self.create_graph(graph_type='hist', new=False)

        self.root.update()

        # TO DO: REFACTOR THIS OUT AT SOME STAGE
        self.total_device_count.configure(text=f"Total Device Count\n{len(x.MACID.unique())}")
        self.total_signal_count.configure(text=f"Total Signal Count\n{x.shape[0]}")

        cutoff = 5

        av_rssi = round(x.RSSI[(time.time() - x.Time) < cutoff].mean(), 1)
        av_sig = round(x[(time.time() - x.Time) < cutoff].shape[0] / 5, 1)
        self.av_rssi.configure(text=f"Average RSSI\n{av_rssi}")
        self.av_signals.configure(text=f"Average Signals per Second\n{av_sig}")

        self.create_hist(new=False)

        if not self.QUIT:
            self.root.after(100, self.update_window)
        else:
            self.root.quit()
            self.root.destroy()

    def update_on_off(self):
        if self.UPDATE:
            self.UPDATE = False
        else:
            self.UPDATE = True

    def update_dropdown(self):
        avs = x.groupby('MACID').mean().sort_values(by="RSSI")
        self.dropdown.configure(values=avs.index.tolist())

    def swap_graph(self):
        if self.GRAPH == "bar":
            self.create_graph(graph_type='hist', new=True)
            self.GRAPH = 'hist'

        else:
            self.create_graph('bar', new=True)
            self.GRAPH = 'bar'

    def create_graph(self, graph_type='bar', new=True):
        '''
        Creates or updates a graph
        :param graph_type: hist or bar
        :param new: Whether the graph is being made for the first time
        '''
        plt.close()

        if graph_type == 'bar':
            avs = x.groupby('MACID').mean().sort_values(by="RSSI", ascending=False)
            avs = avs.iloc[0:15, :]

            if new:
                self.fig, self.ax = plt.subplots()
                plt.subplots_adjust(bottom=0.35)
                self.fig.set_size_inches(11.5, 4.5)
                self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)

            self.ax.bar(avs.index, height=avs.RSSI, label=avs.index, color=self.COLOURS)
            self.ax.set(ylim=(0, -75))
            self.ax.set_title('Average RSSI Values')
            self.ax.set_xticklabels(avs.index, rotation=90, fontsize=10)

            self.canvas.draw()

            if new:
                self.canvas.get_tk_widget().place(relx=0.02, rely=0.48)
            else:
                self.ax.clear()

        elif graph_type == 'hist':
            if new:
                self.fig, self.ax = plt.subplots()
                self.fig.set_size_inches(7.7, 5.5)
                self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)

            self.ax.hist(x.RSSI[x.MACID==self.selected_option], bins=10, lw=1, ec="yellow", fc="green", alpha=0.5)
            self.ax.set(ylim=(0, 15))
            self.canvas.draw()

            if new:
                self.canvas.get_tk_widget().place(relx=0.33, rely=0.025)
            else:
                self.ax.clear()

    def create_hist(self, new=True):
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


    def optionmenu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)

    def quit(self):
        self.QUIT = True

    def create_antenna_hud(self):
        # Put the plot in
        self.create_graph(graph_type='bar', new=True)
        self.create_hist()

        # Add buttons
        # Scan on/off button
        scan_button = ctk.CTkButton(
            master=self.root,
            width=150,
            height=50,
            text="Scan On/Off",
            command=self.update_on_off)

        scan_button.place(relx=0.020, rely=0.02)

        # Hist button
        hist_button = ctk.CTkButton(
            master=self.root,
            width=150,
            height=50,
            text="View: Antenna",
            command=self.swap_graph)

        hist_button.place(relx=0.02, rely=0.1)

        # Quit Button
        quit_button = ctk.CTkButton(
            master=self.root,
            width=150,
            height=50,
            text="Quit",
            command=self.quit)

        quit_button.place(relx=0.02, rely=0.18)

        # Dropdown Selector
        self.selected_option = ctk.StringVar(value="")

        self.dropdown = ctk.CTkOptionMenu(
            master=self.root,
            values=self.MAC_IDS,
            command=self.optionmenu_callback,
            variable=self.selected_option)
        self.dropdown.place(relx=0.025, rely=0.5)

        # Refresh Button
        refresh_button = ctk.CTkButton(
            master=self.root,
            width=150,
            height=30,
            text="Refresh",
            command=self.update_dropdown)
        refresh_button.place(relx=0.15, rely=0.5)

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

# ****************** SCANNER *************************


SCAN_TIME = 20
DEVICE_INTERFACE = 'org.bluez.Device1'
NULL = None

remove_list = set()

x = pd.DataFrame({
    "MACID": [],
    "RSSI": [],
    "Time": []
})


def stop_scan():
    adapter.StopDiscovery()
    mainloop.quit()


def clean_device(rm_dev):
    try:
        adapter.RemoveDevice(rm_dev)
    except GLib.Error as err:
        pass


def on_iface_added(path, interfaces):
    if DEVICE_INTERFACE in interfaces:
        on_device_found(path, interfaces[DEVICE_INTERFACE])


def on_device_found(device_path, device_props):
    global x
    address = device_props.get('Address')
    rssi = device_props.get('RSSI')
    ts = time.time()

    # Stick the data in to our DF
    x = pd.concat([x,
                   pd.Series(
                       {"MACID":address, "RSSI":rssi, "Time":ts}
                   ).to_frame().T],
                  ignore_index=True)

    clean_device(device_path)
    #print(x)


# *********************** ADAPTER SETUP **************************************

bus = SystemBus()
adapter = bus.get('org.bluez', '/org/bluez/hci0')

mngr = bus.get('org.bluez', '/')
mngr.onInterfacesAdded = on_iface_added

mainloop = GLib.MainLoop()


# Change the default scan options
adapter.SetDiscoveryFilter(
    {
        'Transport': GLib.Variant.new_string("le"),
        'DuplicateData': GLib.Variant.new_boolean(True),
        'RSSI': GLib.Variant.new_int16(-70)
    }
)

# ***************************** MAIN PROGRAM **********************************

if __name__ == "__main__":
    adapter.StartDiscovery()
    time.sleep(0.5)
    CTK_Window = ctkApp()

    data = Thread(target=mainloop.run, daemon=True)

    data.start()
    CTK_Window.run()
    plt.close()
    GLib.timeout_add_seconds(0.1, stop_scan)
    data.join()


