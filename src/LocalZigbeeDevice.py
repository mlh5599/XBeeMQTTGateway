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
        
        ResetXBee(config_manager)

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

    ConfigureCoordinator(device, config_manager)
    device.add_io_sample_received_callback(io_sample_received_callback)

def ConfigureCoordinator(device, configuration_manager):

    writeChanges = False
    
    writeChanges = SetPanID(device, configuration_manager)
    
    writeChanges = SetNodeID(device, configuration_manager)

    writeChanges = GetEncryptionEnabled(device, configuration_manager)

    writeChanges = SetEncryptionOptions(device, configuration_manager)

#    if(device.get_node_join_time() != configuration_manager.network_node_join_time):
#        logging.debug("Setting node join time to %s" % configuration_manager.network_node_join_time)
#        device.set_node_join_time(configuration_manager.network_node_join_time)
#        writeChanges = True

    if(writeChanges):
#        device.set_network_encryption_key(configuration_manager.network_encryption_key)
        device.write_changes()

def SetEncryptionOptions(device, configuration_manager):
    """
    Sets the encryption options on the local Zigbee device to the coordinator encryption options.

    Args:
        device (XBeeDevice): The local Zigbee device.
        configuration_manager (ConfigurationManager): The configuration manager.

    Returns:
        bool: True if changes were written to the device, False otherwise.
    """
    device_updated = False
    if(device.get_encryption_options() != configuration_manager.network_encryption_options):
        logging.debug("Setting encryption options to %s" % configuration_manager.network_encryption_options)
        encryption_option_bytes = bytes.fromhex(configuration_manager.network_encryption_options)
        device.set_encryption_options(encryption_option_bytes)
        device_updated = True
    return device_updated


def GetEncryptionEnabled(device, configuration_manager):
    """
    Sets the encryption enabled flag on the local Zigbee device to the coordinator encryption enabled flag.
    
    Args:
        device (XBeeDevice): The local Zigbee device.
        configuration_manager (ConfigurationManager): The configuration manager.
        
    Returns:
            bool: True if changes were written to the device, False otherwise.
    """

    device_updated = False
    if(device.get_encryption_enabled() != configuration_manager.coordinator_encryption_enable):
        logging.debug("Enabling encryption")
        device.set_encryption_enabled(configuration_manager.coordinator_encryption_enable)
        device_updated = True
    return device_updated

def SetPanID(device, configuration_manager):
    """
    Sets the PAN ID of the local Zigbee device to the coordinator PAN ID.

    Args:
        device (XBeeDevice): The local Zigbee device.
        configuration_manager (ConfigurationManager): The configuration manager.

    Returns:
        bool: True if changes were written to the device, False otherwise.
    """
    device_updated = False
    if(device.get_pan_id() != configuration_manager.coordinator_pan_id):
        logging.debug(f'Setting PAN ID to {configuration_manager.coordinator_pan_id}, current ID is {device.get_pan_id()}')
        pan_id_bytes = bytes.fromhex(configuration_manager.coordinator_pan_id)
        device.set_pan_id(pan_id_bytes)
        device_updated = True
    return device_updated

def SetNodeID(device, configuration_manager):
    """
        Set the node ID to the value in the configuration manager if it is not already set

        Arguments:
            device {XBeeDevice} -- The device to set the node ID on
            configuration_manager {ConfigurationManager} -- The configuration manager to get the node ID from

        Returns:
            bool -- True if the node ID was changed, false otherwise
    """
    device_updated = False
    if(device.get_node_id() != configuration_manager.coordinator_node_identifier):

        logging.debug("Setting node ID to Coordinator")
        device.set_node_id(configuration_manager.coordinator_node_identifier)
        device_updated = True
    return device_updated

def SetScanDuration(device, configuration_manager):
    """
    Sets the scan duration of the local Zigbee device to the coordinator scan duration.

    Args:
        device (XBeeDevice): The local Zigbee device.
        configuration_manager (ConfigurationManager): The configuration manager.

    Returns:
        bool: True if changes were written to the device, False otherwise.
    """
    device_updated = False
    if(device.get_scan_duration() != configuration_manager.coordinator_scan_duration):
        logging.debug("Setting scan duration to %s" % configuration_manager.coordinator_scan_duration)
        device.set_scan_duration(configuration_manager.coordinator_scan_duration)
        device_updated = True
    return device_updated


def io_sample_received_callback(io_sample : IOSample, remote_xbee : RemoteXBeeDevice):
    logging.debug("Callback received")
    logging.debug("Calling Device = %s" % remote_xbee.get_64bit_addr())

    device = XBeeDeviceManager.GetRegisteredDevice(str(remote_xbee.get_64bit_addr()))
    
    if device == None:

        device = XBeeDeviceManager.RegisterDevice(io_sample, remote_xbee)

    device.ProcessIncommingIOSample(io_sample)
