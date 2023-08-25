from digi.xbee.devices import XBeeDevice
import XBeeReceive
import MQTTHelper
import XBeeDeviceManager
import pigpio
import time
import sys


def Initialize(device_port, device_baud_rate, io_sample_received_callback, reset_pin, attempt_num=0):

    try:
        attempt_num+=1
        if reset_pin >= 0:
            pi = pigpio.pi()
            
            #Ensure UART is in the correct mode
            pi.set_mode(14, pigpio.ALT0)
            pi.set_mode(15, pigpio.ALT0)

            #Reset the xbee for good measure
            pi.set_mode(reset_pin, pigpio.OUTPUT)
            pi.write(reset_pin,pigpio.LOW)
            time.sleep(1)
            pi.write(reset_pin,pigpio.HIGH)
            time.sleep(2)

        print("Begin session on port %s" % device_port)
        print("Baud rate %s" % device_baud_rate)

        device = XBeeDevice(device_port, device_baud_rate)
        device.open()
        address = device.get_64bit_addr()
        print("Device open, address = %s" %address)

        def data_receive_callback(xbee_message):
            print("Callback received")
            device = XBeeDeviceManager.registered_devices["0013A20040D2A1AC"]
            MQTTHelper.client.publish("myhome/sensors" + device.remote_address.address, "Test Callback")

        device.add_data_received_callback(data_receive_callback)

        device.add_io_sample_received_callback(io_sample_received_callback)

    except:
        if attempt_num < 5:
            print("Unable to connect to xbee, trying again")
            Initialize(device_port, device_baud_rate, io_sample_received_callback, reset_pin, attempt_num)

        print("An error occurred while trying to connect")
        sys.exit(5)