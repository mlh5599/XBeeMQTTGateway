from digi.xbee.devices import XBeeDevice
import XBeeReceive
import MQTTHelper
import XBeeDeviceManager
import pigpio
import time
import sys
from digi.xbee.io import IOSample
from digi.xbee.devices import RemoteXBeeDevice


def Initialize(device_port, device_baud_rate, reset_pin, pi, attempt_num=0):

    try:
        attempt_num+=1
        if reset_pin >= 0:
            
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

        device.add_io_sample_received_callback(io_sample_received_callback)

    except:
        if attempt_num < 5:
            print("Unable to connect to xbee, trying again")
            Initialize(device_port, device_baud_rate, io_sample_received_callback, reset_pin, pi, attempt_num)

        print("An error occurred while trying to connect")
        


def io_sample_received_callback(io_sample : IOSample, remote_xbee : RemoteXBeeDevice, send_time):
    print("Callback received")
    print("Calling Device = %s" % remote_xbee.get_64bit_addr())

    device = XBeeDeviceManager.GetRegisteredDevice(str(remote_xbee.get_64bit_addr()))
    
    if device == None:

        device = XBeeDeviceManager.RegisterDevice(io_sample, remote_xbee)

    device.ProcessIncommingIOSample(io_sample)