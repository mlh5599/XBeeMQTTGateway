import logging
import pigpio
import time




def ResetXBee(configuration_manager):


    if configuration_manager.xbee_reset_pin >= 0:
        logging.debug("Initializing pigpio")
        pi = pigpio.pi()
        logging.debug(f'Ensure UART is in the correct mode')
        #Ensure UART is in the correct mode
        pi.set_mode(14, pigpio.ALT0)
        pi.set_mode(15, pigpio.ALT0)

        logging.debug(f'"Resetting XBee on pin {configuration_manager.xbee_reset_pin}"')
        pi.set_mode(configuration_manager.xbee_reset_pin, pigpio.OUTPUT)
        pi.write(configuration_manager.xbee_reset_pin,pigpio.LOW)
        time.sleep(1)
        pi.write(configuration_manager.xbee_reset_pin,pigpio.HIGH)
        time.sleep(2)