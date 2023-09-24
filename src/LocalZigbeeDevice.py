from digi.xbee.devices import XBeeDevice
import XBeeDeviceManager
from digi.xbee.io import IOSample
from digi.xbee.devices import RemoteXBeeDevice
import logging
from RaspberryPiFunctions import ResetXBee

def Initialize(configuration_manager, attempt_num=0):

    try:
        attempt_num+=1
        logging.debug(f'Initializing Zigbee device - attempt {attempt_num}')
        
        ResetXBee(configuration_manager)

        logging.debug("Begin session on port %s" % configuration_manager.app_config["device_port"])
        logging.debug("Baud rate %s" % configuration_manager.device_baud_rate)

        device = XBeeDevice(configuration_manager.device_port, configuration_manager.device_baud_rate)
        device.open()
        address = device.get_64bit_addr()
        logging.debug("Device open, address = %s" %address)

        ConfigureCoordinator(device, configuration_manager)

        device.add_io_sample_received_callback(io_sample_received_callback)

    except Exception as ex:
        if attempt_num < 5:
            logging.error("Unable to connect to xbee, trying again")
            logging.error(ex)
            Initialize(configuration_manager, attempt_num)
        
        else:
            logging.error("Connecting to xbee failed.  Exiting.")
            raise

def ConfigureCoordinator(configuration_manager, device):

    writeChanges = False
    if(device.get_node_id() != configuration_manager.coordinator_node_identifier):
        logging.debug("Setting node ID to Coordinator")
        device.set_node_id(configuration_manager.coordinator_node_identifier)
        writeChanges = True

    if(device.get_pan_id() != configuration_manager.coordinator_pan_id):
        logging.debug("Setting PAN ID to %s" % configuration_manager.coordinator_pan_id)
        device.set_pan_id(configuration_manager.coordinator_pan_id)
        writeChanges = True

    if(device.get_encryption_enabled() != configuration_manager.coordinator_encryption_enable):
        logging.debug("Enabling encryption")
        device.set_encryption_enabled(configuration_manager.coordinator_encryption_enable)
        writeChanges = True

    if(device.get_encryption_options() != configuration_manager.network_encryption_options):
        logging.debug("Setting encryption options to %s" % configuration_manager.network_encryption_options)
        device.set_encryption_options(configuration_manager.network_encryption_options)
        writeChanges = True

    if(device.get_node_join_time() != configuration_manager.network_node_join_time):
        logging.debug("Setting node join time to %s" % configuration_manager.network_node_join_time)
        device.set_node_join_time(configuration_manager.network_node_join_time)
        writeChanges = True

    if(writeChanges):
        device.set_network_encryption_key(configuration_manager.network_encryption_key)
        device.write_changes()




def io_sample_received_callback(io_sample : IOSample, remote_xbee : RemoteXBeeDevice):
    logging.debug("Callback received")
    logging.debug("Calling Device = %s" % remote_xbee.get_64bit_addr())

    device = XBeeDeviceManager.GetRegisteredDevice(str(remote_xbee.get_64bit_addr()))
    
    if device == None:

        device = XBeeDeviceManager.RegisterDevice(io_sample, remote_xbee)

    device.ProcessIncommingIOSample(io_sample)
