from digi.xbee.devices import XBeeDevice
import XBeeDeviceManager
from digi.xbee.io import IOSample
from digi.xbee.devices import RemoteXBeeDevice
import logging
from PinManipulation import ResetXBee

def Initialize(config_manager):

    attempt_num = 0
    try:
        attempt_num+=1
        logging.debug(f'Initializing Zigbee device - attempt {attempt_num}')
        
        # ResetXBee(configuration_manager)

        logging.debug("Begin session on port %s" % config_manager.app_config["device_port"])
        logging.debug("Baud rate %s" % config_manager.device_baud_rate)

        device = XBeeDevice(config_manager.device_port, config_manager.device_baud_rate)
        device.open()
        address = device.get_64bit_addr()
        logging.debug("Device open, address = %s" %address)

    except Exception as ex:
        if attempt_num < 5:
            logging.error("Unable to connect to xbee, trying again")
            logging.error(ex)
            Initialize(config_manager, attempt_num)
        
        else:
            logging.error("Connecting to xbee failed.  Exiting.")
            raise

        # ConfigureCoordinator(device, config_manager)
        device.add_io_sample_received_callback(io_sample_received_callback)

def ConfigureCoordinator(device, configuration_manager):

    logging.debug(f'PAN_ID = {device.get_pan_id()}')
    writeChanges = False
    if(device.get_node_id() != configuration_manager.coordinator_node_identifier):
        logging.debug("Setting node ID to Coordinator")
        device.set_node_id(configuration_manager.coordinator_node_identifier)
        writeChanges = True

    if(device.get_pan_id() != configuration_manager.coordinator_pan_id):
        logging.debug("Setting PAN ID to %s" % configuration_manager.coordinator_pan_id)
        pan_id_bytes = bytes.fromhex(configuration_manager.coordinator_pan_id)
        device.set_pan_id(pan_id_bytes)
        writeChanges = True

    logging.debug(f'PAN_ID = {device.get_pan_id()}')
    logging.debug(f'Node_ID = {device.get_node_id()}')
#    if(device.get_encryption_enabled() != configuration_manager.coordinator_encryption_enable):
#        logging.debug("Enabling encryption")
#        device.set_encryption_enabled(configuration_manager.coordinator_encryption_enable)
#        writeChanges = True

#    if(device.get_encryption_options() != configuration_manager.network_encryption_options):
#        logging.debug("Setting encryption options to %s" % configuration_manager.network_encryption_options)
#        device.set_encryption_options(configuration_manager.network_encryption_options)
#        writeChanges = True

#    if(device.get_node_join_time() != configuration_manager.network_node_join_time):
#        logging.debug("Setting node join time to %s" % configuration_manager.network_node_join_time)
#        device.set_node_join_time(configuration_manager.network_node_join_time)
#        writeChanges = True

    if(writeChanges):
#        device.set_network_encryption_key(configuration_manager.network_encryption_key)
        device.write_changes()




def io_sample_received_callback(io_sample : IOSample, remote_xbee : RemoteXBeeDevice):
    logging.debug("Callback received")
    logging.debug("Calling Device = %s" % remote_xbee.get_64bit_addr())

    device = XBeeDeviceManager.GetRegisteredDevice(str(remote_xbee.get_64bit_addr()))
    
    if device == None:

        device = XBeeDeviceManager.RegisterDevice(io_sample, remote_xbee)

    device.ProcessIncommingIOSample(io_sample)
