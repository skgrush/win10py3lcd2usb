"""OpenHardwareMonitor screen."""

import time
import logging

from wmi_interfaces.OHM import OHM, get_process, wait_for_process
import lcd2usb

logger = logging.getLogger("ohw")


def getOrWait(lcd: lcd2usb.LCD, timeout: int) -> OHM:
    """Check if OpenHardwareMonitor is running and wait if necessary."""
    while True:
        if not get_process():
            logger.warning("OpenHardwareMonitor not running")

            lcd.clear()
            lcd.fill_center("Waiting for OHM...")
            ret = wait_for_process(timeout)
            if ret:
                logger.info("Found OpenHardwareMonitor")
            else:
                continue

        return OHM()


def screen(lcd: lcd2usb.LCD, update_interval=1):
    """Output information from OpenHardwareMonitor."""
    def looper():
        """Inner loop."""
        ohm = getOrWait(lcd, 60)

        cpu = ohm.first_CPU
        gpu = ohm.first_Gpu
        ram = ohm.first_RAM

        if cpu:
            cpu_load = cpu.getSensor('Load', multiple=True).get(0, None)
            if cpu_load:
                lcd.fill('CPU Load: {:.2%}'.format(cpu_load.Value), 0)
                logger.debug("CPU Load Output")
            else:
                lcd.fill('CPU Load not detected', 0)
                logger.warning("CPU Load not detected")
        else:
            lcd.fill('CPU not detected', 0)
            logger.warning("CPU not detected")

        if ram:
            ram_used = ram.getSensor('Data', multiple=True).get(0, None)
            if ram_used:
                lcd.fill('RAM Used: {:.2f} GB'.format(ram_used.Value), 1)
                logger.debug("RAM Used Output")
            else:
                lcd.fill('RAM Used not detected')
                logger.warning("RAM Used not detected")
        else:
            lcd.fill("RAM not detected", 1)
            logger.warning("RAM not detected")

        if gpu:
            gpu_load = gpu.getSensor('Load', multiple=True).get(0, None)
            gpu_temp = gpu.getSensor('Temperature')
            msgs = ('GPU Load: {:.2%}'.format(gpu_load.Value)
                    if gpu_load else 'GPU Load not detected',
                    'GPU Temp: {:.2f} C'.format(gpu_temp.Value)
                    if gpu_temp else 'GPU Temp not detected')
            lcd.fill(msgs[0], 2)
            lcd.fill(msgs[1], 3)
            if gpu_load and gpu_temp:
                logger.debug("GPU Load/Temp Output")
            else:
                logger.warning("GPU Load/Temp not detected")
        else:
            lcd.fill("GPU not detected", 2)
            lcd.fill("", 3)
            logger.warning("GPU not detected")

    while 1:
        looper()
        time.sleep(update_interval)
