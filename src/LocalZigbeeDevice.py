from digi.xbee.devices import XBeeDevice
import XBeeReceive
import MQTTHelper
import XBeeDeviceManager
import pigpio
import time
import sys
from digi.xbee.io import IOSample
from digi.xbee.devices import RemoteXBeeDevice


def Initialize(configuration_manager, pi, attempt_num=0):

    try:
        attempt_num+=1
        print(f'Initializing Zigbee device - attempt {attempt_num}')
        ResetXBee(configuration_manager, pi)

        print("Begin session on port %s" % configuration_manager.app_config["device_port"])
        print("Baud rate %s" % configuration_manager.device_baud_rate)

        device = XBeeDevice(configuration_manager.device_port, configuration_manager.device_baud_ra
te)
        device.open()
        address = device.get_64bit_addr()
        print("Device open, address = %s" %address)

        device.add_io_sample_received_callback(io_sample_received_callback)

    except Exception as ex:
        if attempt_num < 5:
            print("Unable to connect to xbee, trying again")
            print(ex)
            Initialize(configuration_manager, pi, attempt_num)
        
        else:
            print("An error occurred while trying to connect")
            raise

def ResetXBee(configuration_manager, pi):
    if configuration_manager.xbee_reset_pin >= 0:
        print(f'Ensure UART is in the correct mode')
        #Ensure UART is in the correct mode
        pi.set_mode(14, pigpio.ALT0)
        pi.set_mode(15, pigpio.ALT0)

        print(f'"Resetting XBee on pin {configuration_manager.xbee_reset_pin}"')
        pi.set_mode(configuration_manager.xbee_reset_pin, pigpio.OUTPUT)
        pi.write(configuration_manager.xbee_reset_pin,pigpio.LOW)
        time.sleep(1)
        pi.write(configuration_manager.xbee_reset_pin,pigpio.HIGH)
        time.sleep(2)


def io_sample_received_callback(io_sample : IOSample, remote_xbee : RemoteXBeeDevice):
    print("Callback received")
    print("Calling Device = %s" % remote_xbee.get_64bit_addr())

    device = XBeeDeviceManager.GetRegisteredDevice(str(remote_xbee.get_64bit_addr()))
    
    if device == None:

        device = XBeeDeviceManager.RegisterDevice(io_sample, remote_xbee)

    device.ProcessIncommingIOSample(io_sample)
