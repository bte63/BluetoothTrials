from gi.repository import GLib
from pydbus import SystemBus
from threading import Thread
from BTScanGUI import ctkApp
import matplotlib.pyplot as plt
import time

SCAN_TIME = 10
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
    address = device_props.get('Address')
    rssi = device_props.get('RSSI')

    #if address in our_phones:
    if address in x.keys():
        if len(x[address]) >= 30:
            x[address] = x[address][1:]
            x[address] += [-1*rssi]
        else:
            x[address] += [-1*rssi]

    else:
        x[address] = [-1*rssi]

    clean_device(device_path)
    print(x)


bus = SystemBus()
adapter = bus.get('org.bluez', '/org/bluez/hci0')

# Test
# device = bus.get('org.bluez', '/org/bluez/hci1/dev_44_46_87_C7_D7_3A')

mngr = bus.get('org.bluez', '/')
mngr.onInterfacesAdded = on_iface_added

mainloop = GLib.MainLoop()

GLib.timeout_add_seconds(SCAN_TIME, stop_scan)

# Set up adapter
# adapter.SetDiscoveryFilter({'DuplicateData': GLib.Variant.new_boolean(True)})
adapter.SetDiscoveryFilter(
    {
        'Transport': GLib.Variant.new_string("le"),
        'DuplicateData': GLib.Variant.new_boolean(True),
        'RSSI': GLib.Variant.new_int16(-120)
    }
)

adapter.StartDiscovery()

test = Thread(target=mainloop.run, daemon=True)
test.start()
time.sleep(1)
CTK_Window = ctkApp()
CTK_Window.run()
plt.close()

