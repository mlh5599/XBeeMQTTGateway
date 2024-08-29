import logging
import time
import platform

if platform.system() == 'Linux' and platform.machine() == 'armv7l':
    import pigpio  # pyright: ignore
else:
    import FakePigpio as pigpio


def ResetXBee(configuration_manager):

    if configuration_manager.coordinator_reset_pin >= 0:
        logging.debug("Initializing pigpio")
        pi = pigpio.pi()
        logging.debug('Ensure UART is in the correct mode')
        pi.set_mode(14, pigpio.ALT0)
        pi.set_mode(15, pigpio.ALT0)

        logging.debug(f"Resetting XBee on pin \
                      {configuration_manager.coordinator_reset_pin}")
        pi.set_mode(configuration_manager.coordinator_reset_pin, pigpio.OUTPUT)
        pi.write(configuration_manager.coordinator_reset_pin, pigpio.LOW)
        time.sleep(1)
        pi.write(configuration_manager.coordinator_reset_pin, pigpio.HIGH)
        time.sleep(2)
