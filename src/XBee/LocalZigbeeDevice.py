from digi.xbee.devices import XBeeDevice
import XBee.XBeeDeviceManager as XBeeDeviceManager
from digi.xbee.io import IOSample
from digi.xbee.devices import RemoteXBeeDevice
import logging
from PinManipulation import ResetXBee
import json


def Initialize(config_manager):

    attempt_num = 0
    try:
        attempt_num += 1
        logging.debug(f'Initializing Zigbee device - attempt {attempt_num}')

        ResetXBee(config_manager)

        logging.debug(f"Begin session on port \
                      {config_manager.coordinator_port}")
        logging.debug("Baud rate %s" % config_manager.coordinator_baud_rate)

        device = XBeeDevice(config_manager.coordinator_port,
                            config_manager.coordinator_baud_rate)
        device.open()
        address = device.get_64bit_addr()
        logging.debug(f"Device open, address = {address}")

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

    writeChanges = SetParametersFromConfig(device, configuration_manager)

    if (writeChanges):
        device.set_network_encryption_key(
            configuration_manager.network_encryption_key)
        device.write_changes()


def SetParametersFromConfig(device, configuration_manager):

    coordinator_config_array = \
        configuration_manager.get_coordinator_device_configs()

    print(json.dumps(coordinator_config_array, indent=4))
    writeChanges = False

    for setting in coordinator_config_array:

        key = setting['key']
        value = setting['value']
        type = setting['type']
        read_only = setting['read_only']
        writeChanges = SetLocalDeviceValue(
            device, key, value, type, read_only)

    return writeChanges


def SetLocalDeviceValue(device, key, value, type, read_only):
    """
    Set a value on the local device based on the key and value
    passed in if the device value is different than the value.
    If it is set, the function returns true, otherwise it returns false."""

    device_updated = False

    if (type == "hex"):
        device_updated = SetLocalDeviceValueFromHex(
            device, key, value, read_only)

    # device_value = device.get_parameter(key)
    # if type == "hex":
    #     value_hex = bytes.fromhex(device_value)
    # value_hex = bytes.fromhex(value)
    # logging.info(f"Key: {key} Config: {value_hex}, \
    #             Device: {device_value}")
    # if device_value != value_hex:
    #     logging.info(f"Setting {key} to {value}, \
    #                   current value is {device_value}")
    #     device.set_parameter(key, value)
    #     device_updated = True

    return device_updated


def SetLocalDeviceValueFromHex(device, key, value, read_only):

    device_updated = False
    if (read_only is False):

        print(f"Key: {key}, Value: {value}")
        device_value = device.get_parameter(key)
        device_value = remove_leading_null_bytes(device_value)
        value_bytes = bytearray.fromhex(value[2:])

        if device_value != value_bytes:
            logging.info(f"Setting {key} to {value_bytes}, \
                        current value is {device_value}")
            device.set_parameter(key, value_bytes)
            device_updated = True

    return device_updated


def remove_leading_null_bytes(byte_array):
    # Find the index of the first non-null byte
    first_non_null_index = len(byte_array) - 1
    for i, byte in enumerate(byte_array):
        if byte != 0x00:
            first_non_null_index = i
            break
    # Slice the byte array from the first non-null byte to the end
    return byte_array[first_non_null_index:]


def io_sample_received_callback(io_sample: IOSample,
                                remote_xbee: RemoteXBeeDevice):
    logging.debug("Callback received")
    logging.debug("Calling Device = %s" % remote_xbee.get_64bit_addr())

    device = XBeeDeviceManager.GetRegisteredDevice(
        str(remote_xbee.get_64bit_addr()))

    if device is None:

        device = XBeeDeviceManager.RegisterDevice(io_sample, remote_xbee)

    device.ProcessIncommingIOSample(io_sample)
