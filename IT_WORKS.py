from gi.repository import GLib
from pydbus import SystemBus
from threading import Thread


class Scanner(Thread):
    def __int__(self, scan_time=20, target_devices=[], min_rssi=-120):
        super().__init__()
        self.SCAN_TIME = scan_time
        self.DEVICE_INTERFACE = 'org.bluez.Device1'
        self.bus = SystemBus()
        self.ADAPTER = self.bus.get('org.bluez', '/org/bluez/hci0')
        self.MNGR = self.bus.get('org.bluez', '/')
        self.MNGR.onInterfacesAdded = self.on_interface_added
        self.MIN_RSSI = min_rssi

        self.remove_list = set()
        self.target_devices = target_devices
        self.mainloop = GLib.MainLoop()

        # Set adapter filters
        self.ADAPTER.SetDiscoveryFilter(
            {
                'Transport': GLib.Variant.new_string("le"),
                'DuplicateData': GLib.Variant.new_boolean(True),
                'RSSI': GLib.Variant.new_int16(-120)
            }
        )

    def stop_scan(self):
        self.ADAPTER.StopDiscover()
        self.mainloop.quit()

    def clean_device(self, rm_device):
        try:
            self.ADAPTER.RemoveDevice(rm_device)
        except GLib.Error as err:
            print(err)
            pass

    def on_interface_added(self, path, interfaces):
        if self.MNGR.DEVICE_INTERFACE in interfaces:
            self.on_device_found(path, interfaces[self.MNGR.DEVICE_INTERFACE])

    def on_device_found(self, device_path, device_props):
        address = device_props.get('Address')
        rssi = device_props.get('RSSI')

        print(f'{address} found! RSSI: [{rssi}]')

        self.clean_device(device_path)

    def run(self):
        GLib.timeout_add_seconds(30, self.stop_scan)
        self.ADAPTER.StartDiscover()
        self.mainloop.run()


if __name__ == '__main__':
    test_scanner = Scanner()
    test_scanner.run()



# # def stop_scan():
# #     adapter.StopDiscovery()
# #     mainloop.quit()
# #
# #
# # def clean_device(rm_dev):
# #     try:
# #         adapter.RemoveDevice(rm_dev)
# #     except GLib.Error as err:
# #         pass
#
#
# # def on_iface_added(path, interfaces):
# #     if DEVICE_INTERFACE in interfaces:
# #         on_device_found(path, interfaces[DEVICE_INTERFACE])
#
#
# # def on_device_found(device_path, device_props):
# #     address = device_props.get('Address')
# #     rssi = device_props.get('RSSI')
# #
# #     if address in our_phones:
# #         print(f'{address} found! RSSI: [{rssi}]')
# #
# #     clean_device(device_path)
#
#
# bus = SystemBus()
# adapter = bus.get('org.bluez', '/org/bluez/hci0')
#
# # Test
# # device = bus.get('org.bluez', '/org/bluez/hci1/dev_44_46_87_C7_D7_3A')
#
#
# mngr = bus.get('org.bluez', '/')
# mngr.onInterfacesAdded = on_iface_added
#
# mainloop = GLib.MainLoop()
#
# GLib.timeout_add_seconds(SCAN_TIME, stop_scan)
#
# # Set up adapter
# # adapter.SetDiscoveryFilter({'DuplicateData': GLib.Variant.new_boolean(True)})
# adapter.SetDiscoveryFilter(
#     {
#         'Transport': GLib.Variant.new_string("le"),
#         'DuplicateData': GLib.Variant.new_boolean(True),
#         'RSSI': GLib.Variant.new_int16(-120)
#     }
# )
#
# print(adapter.GetDiscoveryFilters())
# adapter.StartDiscovery()
#
# mainloop.run()