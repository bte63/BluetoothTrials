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
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.root.geometry("1200x900+200x200")
        self.root.title("Dynamic Scatterplot")
        self.UPDATE = True
        self.GRAPH = 'bar'
        self.COLOURS = ["#e50494", "#f77aff", "#7789e1", "#007bc9", "#9dead0",
                        "#7de1ac", "#03b751", "#e9f947", "#cdc90f", "#c5a709"]
        self.MAC_IDS = []

        self.root.update()


        # Put the plot in
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.35)
        self.fig.set_size_inches(7.7, 5.5)
        self.ax.set(ylim=(0, -100))
        self.ax.bar(x.keys(), height=[i[0] for i in x.values()], label=x.keys(), color=self.COLOURS)

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

        # Dropdown Selector
        self.selected_option = ctk.StringVar(value="")
        self.dropdown = ctk.CTkOptionMenu(master=self.root,
                                     values=self.MAC_IDS,
                                     command=self.optionmenu_callback,
                                     variable=self.selected_option)
        self.dropdown.place(relx=0.025, rely=0.5)

        # Refresh Button
        refresh_button = ctk.CTkButton(master=self.root,
                               width=100,
                               height=30,
                               text="Refresh",
                               command=self.update_dropdown)
        refresh_button.place(relx=0.15, rely=0.5)


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
        self.root.after(100, self.update_window)

    def update_on_off(self):
        if self.UPDATE:
            self.UPDATE = False
        else:
            self.UPDATE = True

    def update_dropdown(self):
        avs = pd.DataFrame({"ID": x.keys(), "Vals": [sum(i) / len(i) for i in x.values()]})
        avs.sort_values(by="Vals", ascending=False, inplace=True)
        self.dropdown.configure(values=avs.ID.tolist())

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
            avs = pd.DataFrame({"ID": x.keys(), "Vals": [sum(i) / len(i) for i in x.values()]})
            avs.sort_values(by="Vals", ascending=False, inplace=True)
            avs = avs.iloc[0:10, :]

            if new:
                self.fig, self.ax = plt.subplots()
                plt.subplots_adjust(bottom=0.35)
                self.fig.set_size_inches(7.7, 5.5)
                self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)

            self.ax.bar(avs.ID, height=avs.Vals, label=avs.ID, color=self.COLOURS)
            self.ax.set(ylim=(0, -100))
            self.ax.set_xticklabels(avs.ID, rotation=90)
            self.canvas.draw()

            if new:
                self.canvas.get_tk_widget().place(relx=0.33, rely=0.025)
            else:
                self.ax.clear()

        elif graph_type == 'hist':
            if new:
                self.fig, self.ax = plt.subplots()
                self.fig.set_size_inches(7.7, 5.5)
                self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)

            self.ax.hist(x[self.selected_option.get()], bins=10, lw=1, ec="yellow", fc="green", alpha=0.5)
            self.ax.set(ylim=(0, 10))
            self.canvas.draw()

            if new:
                self.canvas.get_tk_widget().place(relx=0.33, rely=0.025)
            else:
                self.ax.clear()


    def optionmenu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)

    def quit(self):
        self.root.quit()
        self.root.destroy()


# ****************** SCANNER *************************


SCAN_TIME = 20
DEVICE_INTERFACE = 'org.bluez.Device1'
NULL = None

remove_list = set()

our_phones = ["61:2B:70:B2:AA:37", "44:46:87:C7:D7:3A"]

x = {}

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

    #if address in our_phones:
    if address in x.keys():
        if len(x[address]) >= 50:
            x[address] = x[address][1:]
            x[address] += [rssi]
        else:
            x[address] += [rssi]

    else:
        x[address] = [rssi]

    clean_device(device_path)
    #print(x)


bus = SystemBus()
adapter = bus.get('org.bluez', '/org/bluez/hci0')

# Test
# device = bus.get('org.bluez', '/org/bluez/hci1/dev_44_46_87_C7_D7_3A')

mngr = bus.get('org.bluez', '/')
mngr.onInterfacesAdded = on_iface_added

mainloop = GLib.MainLoop()


# Set up adapter
adapter.SetDiscoveryFilter(
    {
        'Transport': GLib.Variant.new_string("le"),
        'DuplicateData': GLib.Variant.new_boolean(True),
        'RSSI': GLib.Variant.new_int16(-70)
    }
)


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


