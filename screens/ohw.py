"""OpenHardwareMonitor screen."""

import time
import logging

from wmi_interfaces.OHM import OHM, get_process, wait_for_process
import lcd2usb


logger = logging.getLogger("ohw")


def getOrWait(lcd: lcd2usb.LCD, timeout: int) -> int:
    """Check if OpenHardwareMonitor is running and wait if necessary.

    Returns
    -------
        (int) the process ID of OHM.

    """
    while True:
        proc = get_process()
        if not proc:
            logger.warning("OpenHardwareMonitor not running")

            lcd.clear()
            lcd.fill_center("Waiting for OHM...")

            proc = wait_for_process(timeout)
            if not (proc and proc.ProcessId):
                continue

            logger.info("Found OpenHardwareMonitor")

        return proc.ProcessId


def screen(lcd: lcd2usb.LCD, update_interval=1):
    """Output information from OpenHardwareMonitor."""
    ohm = None
    ohm_pid = None

    while 1:
        _new_pid = getOrWait(lcd, 60)
        if ohm_pid != _new_pid:
            ohm_pid = _new_pid
            ohm = OHM()

        _cpu(ohm.first_CPU, lcd)
        _gpu(ohm.first_Gpu, lcd)
        _ram(ohm.first_RAM, lcd)

        time.sleep(update_interval)


def _cpu(cpu, lcd: lcd2usb.LCD):
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


def _ram(ram, lcd: lcd2usb.LCD):
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


def _gpu(gpu, lcd: lcd2usb.LCD):
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
