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
        return self.app_config.get("coordinator", {})["port"]
    
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
        return self.app_config.get("coordinator", {}).get("baud_rate", 9600)
    
    @property
    def coordinator_pan_id(self):
        """
        Set the PAN (Personal Area Network) ID for the network (ZigBee extended PAN ID). 
        Valid range is 0 - 0xFFFFFFFFFFFFFFFF. (Default: 0)
        Alternatively, set ID=0 for the coordinator to choose a random Pan ID.
        """
        return self.app_config.get("coordinator",{}).get("pan_id", "0")
    
    @property
    def coordinator_scan_channels(self):
        """
        Set/read list of channels to scan (active and energy scans) when 
        forming a PAN as bitfield. Scans are initiated during coordinator 
        startup: Bit 15 = Chan 0x1A . . . Bit 0 = Chan 0x0B
        Valid range is 0 - 0xFFFF (Default: FFFF)
        """
        return self.app_config.get("coordinator", {}).get("scan_channels", "FFFF")
    
    @property
    def coordinator_scan_duration(self):
        """
        Set/read the Scan Duration exponent. The exponent configures the duration 
        of the active scan and energy scan during coordinator initialization. 
        Scan Time = SC * (2 ^ SD) * 15.36ms. (SC=# channels)
        Valid range is 0x0 - 0x07 (Default: 3)
        """
        return self.app_config.get("coordinator", {}).get("scan_duration", "3")

    @property
    def coordinator_zigbee_stack_profile(self):
        """
        Set/read the ZigBee stack profile setting. 0=Network Specific, 1=ZigBee-2006, 2=ZigBee-PRO
        Range: 0x0 - 0x2 (Default: 0)
        """
        return self.app_config.get("coordinator", {}).get("zigbee_stack_profile", "0")
    
    @property
    def coordinator_node_join_time(self):
        """
        Set/read the Node Join time. The value of NJ determines the time (in seconds) 
        that the device will allow other devices to join to it. If set to 0xFF, 
        the device will always allow joining.
        Range: 0x0 - 0xFF (Default: FF)
        """
        return self.app_config.get("coordinator", {}).get("node_join_time", "FF")

    @property
    def coordinator_destination_address_high(self):
        """
        Set/read the upper 32 bits of the 64 bit destination extended address. 
        0x000000000000FFFF is the broadcast address for the PAN. 
        0x0000000000000000 can be used to address the Pan Coordinator.
        Range: 0x0 - 0xFFFFFFFF (Default 0)
        """
        return self.app_config.get("coordinator", {}).get("destination_address_high", "0")

    @property
    def coordinator_destination_address_low(self):
        """
        Set/read the lower 32 bits of the 64 bit destination extended address. 
        0x000000000000FFFF is the broadcast address for the PAN. 
        0x0000000000000000 can be used to address the Pan Coordinator.
        Range: 0x0 - 0xFFFFFFFF (Default FFFF)
        """
        return self.app_config.get("coordinator", {}).get("destination_address_low", "FFFF")

    @property
    def coordinator_node_identifier(self):
        """
        Set/read Node Identifier string
        0-20 ASCII characters (Default '')
        """
        return self.app_config.get("coordinator", {}).get("node_identifier", '')
    
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
        return self.app_config.get("coordinator", {}).get("maximum_hops", "1e")

    @property
    def coordinator_broadcast_radius(self):
        """
        Set/Read the transmission radius for broadcast data transmissions. 
        Set to 0 for maximum radius.
        Range 0x0 - 0x1E (Default: FF)
        """
        return self.app_config.get("coordinator", {}).get("broadcast_radius","FF")

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
        return self.app_config.get("coordinator", {}).get("many_to_one_broadcast_time","FF")

    @property
    def coordinator_device_type_identifier(self):
        """
        Set/read the device type identifier value. 
        This can be used to differentiate multiple XBee-based products.
        Range 0x0 - 0xFFFFFFFF (Default: 3000)
        """
        return self.app_config.get("coordinator", {}).get("device_type_identifier","3000")

    @property
    def coordinator_node_discovery_backoff(self):
        """
        Set/read Node Discovery backoff register.
        This sets the maximum delay for Node Discovery responses to be sent (ND, DN).
        Range 0x20 - 0xFF (Default: 3C)
        """
        return self.app_config.get("coordinator", {}).get("node_discovery_backoff","3C")

    @property
    def coordinator_node_doscovery_options(self):
        """
        Sets the node discovery options register. Options include 0x01 - Append DD value 
        to end of node discovery, 0x02 - Return devices own ND response first.
        Range 0x0 - 0x3 (Default: 0)
        """
        return self.app_config.get("coordinator", {}).get("node_discovery_options","0")
    
    @property
    def coordinator_pan_conflict_threshold(self):
        """
        Set/read threshold for the number of PAN id conflict reports that must be 
        received by the network manager within one minute to trigger a PAN id change.
        Range 0x1 - 0x3F (Default: 3)
        """
        return self.app_config.get("coordinator", {}).get("pan_conflict_threshold","3")
    
    @property
    def coordinator_power_level(self):
        """
        Select/Read transmitter output power. Power levels relative to 
        PP: 0=-10dB, 1=-6dB, 2=-4dB, 3=-2dB, 4=0dB.
        Range 0x0 - 0x4 (Default: 4)
        """
        return self.app_config.get("coordinator", {}).get("power_level","4")
    
    @property
    def coordinator_power_mode(self):
        """
        Select/Read module boost mode setting. If enabled, boost mode improves 
        sensitivity by 1dB and increases output power by 2dB, improving the link 
        margin and range.
        Default: 1
        """
        return self.app_config.get("coordinator", {}).get("power_mode","1")
    
    @property
    def coordinator_encryption_enable(self):
        """
        Enable or disable ZigBee encryption.
        Default: 0
        """
        return self.app_config.get("coordinator", {}).get("encryption_enable","0")
    
    
    @property
    def coordinator_encryption_options(self):
        """
        Set the ZigBee Encryption options: Bit0 = Acquire / Transmit network 
        security key unencrypted during joining, Bit1 = Use Trust Center.
        Range 0x0 - 0x3 (Default: 0)
        """
        return self.app_config.get("coordinator", {}).get("encryption_options","0")
    
    @property
    def coordinator_encryption_key(self):
        """
        Sets key used for encryption and decryption (ZigBee trust center link key). 
        This register can not be read.
        0 - 32 hexadecimal characters (Default: '')
        """
        return self.app_config.get("coordinator", {}).get("encryption_key", "")
    
    @property
    def coordinator_network_encryption_key(self):
        """
        Sets network key used for network encryption and decryption. 
        If set to 0 (default), the coordinator selects a random network encryption 
        key (recommended). This register can not be read.
        0 - 32 hexadecimal characters (Default: '')
        """
        return self.app_config.get("coordinator", {}).get("network_encryption_key", "")
    
    @property
    def coordinator_parity(self):
        """
        Set/read the serial interface parity. 0=none, 1=even, 2=odd.
        Range 0x0 - 0x2 (Default: 0)
        """
        return self.app_config.get("coordinator", {}).get("parity","0")
    
    @property
    def coordinator_stop_bits(self):
        """
        Set/read the serial interface stop bits. 0=1 stop bit, 1=2 stop bits.
        Range 0x0 - 0x1 (Default: 0)
        """
        return self.app_config.get("coordinator", {}).get("stop_bits","0")

    @property
    def coordinator_DIO7_configuration(self):
        """
        Configure options for the DIO7 line of the module. 
        Options include: CTS flow control, Digital Input and Output, or RS-485 enable control.
        0 = Disable
        1 = CTS flow control
        2 = N/A
        3 = Digital Input
        4 = Digital Output Low
        5 = Digital Output High
        6 = RS-485 Enable Low
        7 = RS-485 Enable High
        Default = 1
        """
        return self.app_config.get("coordinator", {}).get("DIO7_configuration","1")

    @property
    def coordinator_DIO6_configuration(self):
        """
        Configure options for the DIO6 line of the module. 
        Options include: RTS flow control, Digital Input and Output, or RS-485 direction control.
        0 = Disable
        1 = CTS flow control
        2 = N/A
        3 = Digital Input
        4 = Digital Output Low
        5 = Digital Output High
        Default = 0
        """
        return self.app_config.get("coordinator", {}).get("DIO6_configuration","1")

    @property
    def coordinator_API_enable(self):
        """
        Enable or disable API mode.
        1 = API enabled
        2 = API enabled, with escaped characters
        Default: 1
        """
        return self.app_config.get("coordinator", {}).get("API_enable","1")

    @property
    def coordinator_API_output_mode(self):
        """
        Set the API output mode register value. 0 - Received Data formatted as native API 
        frame format. 1 - Received RF data formatted as Explicit Rx-Indicator. 3 - Same as 1,
          plus received ZDO requests are passed out the UART.
        Default: 0
        """
        return self.app_config.get("coordinator", {}).get("API_output_mode","0")
    
    @property
    def coordinator_cyclic_sleep_period(self):
        """
        Set/read Cyclic sleep period for cyclic sleeping remotes. Set SP on parent 
        (Coordinator or Router) to match the largest SP of its end device children. 
        On a router or coordinator, SP determines the transmission timeout when sending 
        to a sleeping end device. SP also determines how long the parent will buffer a 
        message for a sleeping child.
        Range 0x20 - 0xAF0 (Default: 20)
        """
        return self.app_config.get("coordinator", {}).get("cyclic_sleep_period","20")
    
    @property
    def coordinator_number_of_cyclic_sleep_periods(self):
        """
        Set/read the number of cyclic sleep periods used to calculate end device poll 
        timeout. If an end device does not send a poll request to its parent coordinator 
        or router within the poll timeout, the end device is removed from the child table. 
        The poll timeout is calculated in milliseconds as (3 * SN * (SP * 10ms)), minimum 
        of 5 seconds. i.e. if SN=15, SP=0x64, the timeout is 45 seconds.
        Range 0x1 - 0xFFFF (Default: 1)
        """
        return self.app_config.get("coordinator", {}).get("number_of_cyclic_sleep_periods","1")
    
    @property
    def coordinator_AD0_DIO0_configuration(self):
        """
        Configure options for the AD0/DIO0 line of the module. Options include: Enabling 
        commissioning button functionality, Analog to Digital converter,Digital Input 
        and Output.
        0 = Disabled
        1 = Commissioning Button
        2 = Analog to Digital converter
        3 = Digital Input
        4 = Digital Output Low
        5 = Digital Output High
        Default: 1
        """
        return self.app_config.get("coordinator", {}).get("AD0_DIO0_configuration","1")

    @property
    def coordinator_AD1_DIO1_configuration(self):
        """
        Configure options for the AD1/DIO1 line of the module. Options include: 
        Analog to Digital converter, Digital Input and Output.
        0 = Disabled
        1 = N/A
        2 = Analog to Digital converter
        3 = Digital Input
        4 = Digital Output Low
        5 = Digital Output High
        Default: 0
        """
        return self.app_config.get("coordinator", {}).get("AD1_DIO1_configuration","0")

    @property
    def coordinator_AD2_DIO2_configuration(self):
        """
        Configure options for the AD2/DIO2 line of the module. Options include: 
        Analog to Digital converter, Digital Input and Output.
        0 = Disabled
        1 = N/A
        2 = Analog to Digital converter
        3 = Digital Input
        4 = Digital Output Low
        5 = Digital Output High
        Default: 0
        """
        return self.app_config.get("coordinator", {}).get("AD2_DIO2_configuration","0")
    
    @property
    def coordinator_AD3_DIO3_configuration(self):
        """
        Configure options for the AD3/DIO3 line of the module. Options include: 
        Analog to Digital converter, Digital Input and Output.
        0 = Disabled
        1 = N/A
        2 = Analog to Digital converter
        3 = Digital Input
        4 = Digital Output Low
        5 = Digital Output High
        Default: 0
        """
        return self.app_config.get("coordinator", {}).get("AD3_DIO3_configuration","0")


    @property
    def coordinator_DIO4_configuration(self):
        """
        Configure options for the AD4/DIO4 line of the module. Options include: 
        Digital Input and Output.
        0 = Disabled
        1 = N/A
        2 = N/A
        3 = Digital Input
        4 = Digital Output Low
        5 = Digital Output High
        Default: 0
        """
        return self.app_config.get("coordinator", {}).get("DIO4_configuration", "0")

    @property
    def coordinator_DIO5_configuration(self):
        """
        Configure options for the DIO5/Assoc line of the module. 
        Options include: Associated LED indicator (blinks when associated),Digital 
        Input and Output.
        0 = Disabled
        1 = Associated Indicator
        2 = N/A
        3 = Digital Input
        4 = Digital Output Low
        5 = Digital Output High
        Default: 1
        """
        return self.app_config.get("coordinator", {}).get("DIO5_configuration", "1")

    @property
    def coordinator_DIO10_PWM0_configuration(self):
        """
        Configure options for the DIO10/PWM0 line of the module. Options include: 
        Digital Input and Output, Pulse Width Modulation.
        0 = Disabled
        1 = RSSI PWM Output
        2 = N/A
        3 = Digital Input
        4 = Digital Output Low
        5 = Digital Output High
        Default: 1
        """
        return self.app_config.get("coordinator", {}).get("DIO10_PWM0_configuration", "1")

    @property
    def coordinator_DIO11_configuration(self):
        """
        Configure options for the DIO11 line of the module. Options include: 
        Digital Input and Output.
        0 = Disabled
        1 = N/A
        2 = N/A
        3 = Digital Input
        4 = Digital Output Low
        5 = Digital Output High
        Default: 0
        """
        return self.app_config.get("coordinator", {}).get("DIO11_configuration", "0")

    @property
    def coordinator_DIO12_configuration(self):
        """
        Configure options for the DIO12 line of the module. Options include: 
        Digital Input and Output.
        0 = Disabled
        1 = N/A
        2 = N/A
        3 = Digital Input
        4 = Digital Output Low
        5 = Digital Output High
        Default: 0
        """
        return self.app_config.get("coordinator", {}).get("DIO12_configuration", "0")


    @property
    def coordinator_pull_up_resistor_enable(self):
        """
        Set/read bitfield to configure internal pullup resistors status for I/O lines. 
        1=internal pullup enabled, 0=no internal pullup. 
        Bitfield map: 
        (13)DIO7/CTS, (12)-DIO11, (11)-DIO10/PWM0, (10)-DIO12, (9)-On/Sleep, 
        (8)Associate, (7)-DIN/Config, (6)-Sleep_Rq, (5)-RTS, (4)-AD0/DIO0, 
        (3)-AD1/DIO1, (2)-AD2/DIO2, (1)-AD3/DIO3, (0)-DIO4
        Range 0x0 - 0x3FFF (Default: 1FFF)
        """
        return self.app_config.get("coordinator", {}).get("pull_up_resistor_enable", "1FFF")
    
    @property
    def coordinator_associate_LED_blink_time(self):
        """
        Set/read the Associate LED blink rate. This value determines the 
        blink rate of the Associate/DIO5 pin if D5=1 and the module has started a 
        network. Setting LT to 0 will use the default blink time (500ms).
        Range 0x0A - 0xFF (Default: 0)
        """
        return self.app_config.get("coordinator", {}).get("associate_LED_blink_time", "0")
    
    @property
    def coordinator_rssi_pwm_timer(self):
        """
        Set/read PWM timer register. Set duration of PWM (pulse width modulation) 
        signal output on the RSSI pin (P6). The signal duty cycle is updated with 
        each received packet or APS acknowledgment and is shut off when the timer expires.
        Range 0x0 - 0xFF (Default: 28)
        """
        return self.app_config.get("coordinator", {}).get("rssi_pwm_timer", "28")
    
    @property
    def coordinator_device_options(self):
        """
        Bit0 - Reserved. Bit1 - Reserved. Bit2 - Reserved. Bit3 - Disable NULL Transport Key.
        Range 0x0 - 0xFF (Default: 1)
        """
        return self.app_config.get("coordinator", {}).get("device_options", "1")

    @property
    def coordinator_IO_sampling_rate(self):
        """
        Set the IO sampling rate to enable periodic sampling. If set >0, all enabled 
        digital IO and analog inputs will be sampled and transmitted every IR milliseconds. 
        IO Samples are transmitted to the address specified by DH+DL.
        Range 0x32 - 0xFFFF (Default: 0)
        """
        return self.app_config.get("coordinator", {}).get("IO_sampling_rate", "0")
    
    @property
    def coordinator_digital_IO_change_detection(self):
        """
        Bitfield that configures which digital IO pins should be monitored for change
        detection. If a change is detected on an enabled digital IO pin, a digital IO
        sample is immediately transmitted to the address specified by DH+DL.
        Range 0x0 - 0xFFFF (Default: 0)
        """
        return self.app_config.get("coordinator", {}).get("digital_IO_change_detection", "0")
    
    @property
    def coordinator_supply_voltage_high_threshold(self):
        """
        Set/read the supply voltage high threshold. If the supply voltage is above 
        this threshold, the module will set the supply voltage high bit in the 
        IO sample packet. The supply voltage is sampled every 1.1 seconds.
        Range 0x0 - 0xFFFF (Default: 0)
        """
        return self.app_config.get("coordinator", {}).get("supply_voltage_high_threshold", "0")
    @property
    def mqtt_broker(self):
        return self.app_config["mqtt_broker"]
    
    @property
    def mqtt_port(self):
        return self.app_config["mqtt_port"] 
    
    @property
    def coordinator_reset_pin(self):
        return self.app_config.get("coordinator", {})["reset_pin"]
    
    @property
    def status_light_pin(self):
        return self.app_config["status_light_pin"]
    
    @property
    def log_level(self):
        return self.app_config["log_level"]
    