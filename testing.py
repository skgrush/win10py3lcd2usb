#!/usr/bin/env python3

import datetime
import time

try:
    import lcd2usb
except ImportError:
    from lib import lcd2usb


import atexitLCD


def basic(lcd: lcd2usb.LCD):
    bus, dev = lcd.info(False)
    version = lcd.version
    now = datetime.datetime.now()
    lcd.clear()
    lcd.fill('LCD Version: {0}.{1}'.format(*version), 0)
    lcd.fill('Bus: {0:x}, Dev: {1:x}'.format(bus, dev), 1)
    lcd.fill(str(now), 2)
    lcd.fill_center('win10py3lcd2usb', 3)


def openhardwaremonitor(lcd: lcd2usb.LCD, update_interval=1):

    from wmi_interfaces.OHM import OHM, get_process

    if not get_process():
        raise RuntimeError("OpenHardwareMonitor not running")

    ohm = OHM()

    def looper():
        if not get_process():
            lcd.fill_center("OHM not running")
            for i in range(1, 4):
                lcd.fill('', i)

        else:
            cpu = ohm.first_CPU
            gpu = ohm.first_Gpu
            ram = ohm.first_RAM

            if cpu:
                cpu_load = cpu.getSensor('Load', multiple=True).get(0, None)
                if cpu_load:
                    lcd.fill('CPU Load: {:.2%}'.format(cpu_load.Value), 0)
                else:
                    lcd.fill('CPU Load not detected', 0)

            if ram:
                ram_used = ram.getSensor('Data', multiple=True).get(0, None)
                msg = 'RAM Used: {:.2f} GB'.format(ram_used.Value) if ram_used \
                      else 'RAM Used not detected'
                lcd.fill(msg, 1)

            if gpu:
                gpu_load = gpu.getSensor('Load', multiple=True).get(0, None)
                gpu_temp = gpu.getSensor('Temperature')
                msgs = ('GPU Load: {:.2%}'.format(gpu_load.Value) \
                        if gpu_load else 'GPU Load not detected',
                        'GPU Temp: {:.2f} C'.format(gpu_temp.Value)
                        if gpu_temp else 'GPU Temp not detected')
                lcd.fill(msgs[0], 2)
                lcd.fill(msgs[1], 3)

    while(1):
        looper()
        time.sleep(update_interval)


if __name__ == '__main__':

    try:
        openhardwaremonitor(lcd2usb.LCD(), 0.5)
    except KeyboardInterrupt:
        pass
    except:
        import traceback
        traceback.print_exc()
        input("Hit enter to exit:")
