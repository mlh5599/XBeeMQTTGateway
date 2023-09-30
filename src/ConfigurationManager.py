import json
import logging

class ConfigurationManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.app_config = {}


    def load_config(self):
        try:
            logging.debug(f"Loading config from '{self.config_path}'")
            with open(self.config_path, 'r') as config_file:
                self.app_config = json.load(config_file)
            logging.debug(f"Config loaded: {self.app_config}")


        except FileNotFoundError:
            logging.error(f"Config file '{self.config_path}' not found.")
            raise
        except Exception as ex:
            logging.error(f"Error loading config from '{self.config_path}': {ex}")
            raise
    
    # def get_config(self):
    #     return self.app_config
    
    @property
    def coordinator_port(self):
        return self.app_config["coordinator"]["port"]
    
    @property
    def coordinator_baud_rate(self):
        """
         the serial interface baud rate for communication between modem serial port 
         and host. Request non-standard baud rates above 0x12C using a terminal window. 
         Read BD register to find actual baud rate achieved.
         0 - 1200
         1 - 2400
         2 - 4800
         3 - 9600
         4 - 19200
         5 - 38400
         6 - 57600
         7 - 115200
         Default: 3
         """
        return self.app_config["coordinator"].get("baud_rate", 9600)
    
    @property
    def coordinator_pan_id(self):
        """
        Set the PAN (Personal Area Network) ID for the network (ZigBee extended PAN ID). 
        Valid range is 0 - 0xFFFFFFFFFFFFFFFF. (Default: 0)
        Alternatively, set ID=0 for the coordinator to choose a random Pan ID.
        """
        return self.app_config["coordinator"].get("pan_id", 0)
    
    @property
    def coordinator_scan_channels(self):
        """
        Set/read list of channels to scan (active and energy scans) when 
        forming a PAN as bitfield. Scans are initiated during coordinator 
        startup: Bit 15 = Chan 0x1A . . . Bit 0 = Chan 0x0B
        Valid range is 0 - 0xFFFF (Default: FFFF)
        """
        return self.app_config["coordinator"].get("scan_channels", 0xFFFF)
    
    @property
    def coordinator_scan_duration(self):
        """
        Set/read the Scan Duration exponent. The exponent configures the duration 
        of the active scan and energy scan during coordinator initialization. 
        Scan Time = SC * (2 ^ SD) * 15.36ms. (SC=# channels)
        Valid range is 0x0 - 0x07 (Default: 3)
        """
        return self.app_config["coordinator"].get("scan_duration", "3")

    @property
    def coordinator_zigbee_stack_profile(self):
        """
        Set/read the ZigBee stack profile setting. 0=Network Specific, 1=ZigBee-2006, 2=ZigBee-PRO
        Range: 0x0 - 0x2 (Default: 0)
        """
        return self.app_config["coordinator"].get("zigbee_stack_profile", "0")
    
    @property
    def coordinator_node_join_time(self):
        """
        Set/read the Node Join time. The value of NJ determines the time (in seconds) 
        that the device will allow other devices to join to it. If set to 0xFF, 
        the device will always allow joining.
        Range: 0x0 - 0xFF (Default: FF)
        """
        return self.app_config["coordinator"].get("node_join_time", "FF")

    @property
    def coordinator_destination_address_high(self):
        """
        Set/read the upper 32 bits of the 64 bit destination extended address. 
        0x000000000000FFFF is the broadcast address for the PAN. 
        0x0000000000000000 can be used to address the Pan Coordinator.
        Range: 0x0 - 0xFFFFFFFF (Default 0)
        """
        return self.app_config["coordinator"].get("destination_address_high")

    @property
    def coordinator_destination_address_low(self):
        """
        Set/read the lower 32 bits of the 64 bit destination extended address. 
        0x000000000000FFFF is the broadcast address for the PAN. 
        0x0000000000000000 can be used to address the Pan Coordinator.
        Range: 0x0 - 0xFFFFFFFF (Default FFFF)
        """
        return self.app_config["coordinator"].get("destination_address_low")

    @property
    def coordinator_node_identifier(self):
        """
        Set/read Node Identifier string
        0-20 ASCII characters (Default '')
        """
        return self.app_config["coordinator"].get("node_identifier", '""')
    
    @property
    def coordinator_maximum_hops(self):
        """
        Set/read the maximum hops limit. This limit sets the maximum number of 
        broadcast hops (BH) and determines the unicast timeout 
        (unicast timeout = (50 * NH) + 100). 
        A unicast timeout of 1.6 seconds (NH=30) is enough time for the data 
        and acknowledgment to traverse about 8 hops.
        Range: 0x0 - 0xFF (Default 1e)
        """
        return self.app_config["coordinator"].get("maximum_hops", "1e")

    @property
    def coordinator_broadcast_radius(self):
        """
        Set/Read the transmission radius for broadcast data transmissions. 
        Set to 0 for maximum radius.
        Range 0x0 - 0x1E (Default: FF)
        """
        return self.app_config["coordinator"].get("broadcast_radius","FF")

    @property
    def coordinator_many_to_one_broadcast_time(self):
        """
        Set/read the time between aggregation route broadcast times. 
        An aggregation route broadcast creates a route on all devices in the 
        network back to the device that sends the aggregation broadcast. 
        Setting AR to 0xFF disables aggregation route broadcasting. 
        Setting AR to 0 sends one broadcast.
        Range 0x0 - 0xFF (Default: FF)
        """
        return self.app_config["coordinator"].get("many_to_one_broadcast_radius","FF")

    @property
    def coordinator_device_type_identifier(self):
        """
        Set/read the device type identifier value. 
        This can be used to differentiate multiple XBee-based products.
        Range 0x0 - 0xFFFFFFFF (Default: 3000)
        """
        return self.app_config["coordinator"].get("device_type_identifier","3000")

    @property
    def coordinator_node_discovery_backoff(self):
        """
        Set/read Node Discovery backoff register.
        This sets the maximum delay for Node Discovery responses to be sent (ND, DN).
        Range 0x20 - 0xFF (Default: 3C)
        """
        return self.app_config["coordinator"].get("node_discovery_backoff","3C")

    @property
    def coordinator_node_doscovery_options(self):
        """
        Sets the node discovery options register. Options include 0x01 - Append DD value 
        to end of node discovery, 0x02 - Return devices own ND response first.
        Range 0x0 - 0x3 (Default: 0)
        """
        return self.app_config["coordinator"].get("node_discovery_options","0")
    
    @property
    def coordinator_pan_conflict_threshold(self):
        """
        Set/read threshold for the number of PAN id conflict reports that must be 
        received by the network manager within one minute to trigger a PAN id change.
        Range 0x1 - 0x3F (Default: 3)
        """
        return self.app_config["coordinator"].get("pan_conflict_threshold","3")
    
    @property
    def coordinator_power_level(self):
        """
        Select/Read transmitter output power. Power levels relative to 
        PP: 0=-10dB, 1=-6dB, 2=-4dB, 3=-2dB, 4=0dB.
        Range 0x0 - 0x4 (Default: 4)
        """
        return self.app_config["coordinator"].get("power_level","4")
    
    @property
    def coordinator_power_mode(self):
        """
        Select/Read module boost mode setting. If enabled, boost mode improves 
        sensitivity by 1dB and increases output power by 2dB, improving the link 
        margin and range.
        Default: 1
        """
        return self.app_config["coordinator"].get("power_mode","1")
    
    @property
    def coordinator_encryption_enable(self):
        """
        Enable or disable ZigBee encryption.
        Default: 0
        """
        return self.app_config["coordinator"].get("encryption_enable","0")
    
    
    @property
    def coordinator_encryption_options(self):
        """
        Set the ZigBee Encryption options: Bit0 = Acquire / Transmit network 
        security key unencrypted during joining, Bit1 = Use Trust Center.
        Range 0x0 - 0x3 (Default: 0)
        """
        return self.app_config["coordinator"].get("encryption_options","0")
    
    @property
    def coordinator_encryption_key(self):
        """
        Sets key used for encryption and decryption (ZigBee trust center link key). 
        This register can not be read.
        0 - 32 hexadecimal characters (Default: '')
        """
        return self.app_config["coordinator"].get("encryption_key",'""')
    
    @property
    def coordinator_network_encryption_key(self):
        """
        Sets network key used for network encryption and decryption. 
        If set to 0 (default), the coordinator selects a random network encryption 
        key (recommended). This register can not be read.
        0 - 32 hexadecimal characters (Default: '')
        """
        return self.app_config["coordinator"].get("network_encryption_key",'""')
    
    @property
    def mqtt_broker(self):
        return self.app_config["mqtt_broker"]
    
    @property
    def mqtt_port(self):
        return self.app_config["mqtt_port"] 
    
    @property
    def coordinator_reset_pin(self):
        return self.app_config["coordinator"]["reset_pin"]
    
    @property
    def status_light_pin(self):
        return self.app_config["status_light_pin"]
    
    @property
    def log_level(self):
        return self.app_config["log_level"]
    