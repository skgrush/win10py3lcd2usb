
import enum
from operator import itemgetter
import warnings

import wmi

EXE_NAME = "OpenHardwareMonitor.exe"
NAMESPACE = "root/OpenHardwareMonitor"

KNOWN_HW_TYPES = (
    'Mainboard',
    'SuperIO',
    'CPU',
    'GpuNvidia',
    'GpuAti',
    'TBalancer',
    'Heatmaster',
    'HDD',
    'RAM'
)

KNOWN_SENSOR_TYPES = (
    'Voltage',  # Volt (V)
    'Clock',  # Megahertz (MHz)
    'Temperature',  # Degrees Celsius (°C)
    'Load',  # (%)
    'Fan',  # (RPM)
    'Flow',  # Liters per hour (L/h)
    'Control',  # (%)
    'Level',  # (%)
    'Data',  # Gigabytes? (GB)
)

KNOWN_SENSOR_TYPE_UNITS = (
    ' V',
    ' MHz',
    ' °C',
    '%',
    ' RPM',
    ' L/h',
    '%',
    '%',
    ' GB',
)


class NotFoundException(RuntimeError):
    def __init__(self, typ, selectors):
        self.type, self.selectors = typ, selectors
        self.message = "Failed to find {.__name__} with selectors {}".format(
                       typ, selectors)
        super().__init__(self.message)


class OHMWarning(RuntimeWarning, UserWarning):
    pass


class MultipleFoundWarning(OHMWarning):
    def __init__(self, typ, selectors):
        self.type, self.selectors = typ, selectors
        self.message = "Found multiple {.__name__} with selectors {}".format(
                       typ, selectors)
        super().__init__(self.message)


class WmiAttributeError(RuntimeError):
    def __init__(self, typ, attribute):
        self.type, self.attribute = typ, attribute
        self.message = "Failed to retrieve {.__name__} attribute(s) {}".format(
                       typ, attribute)
        super().__init__(self.message)


def get_process(c: wmi.WMI = wmi.WMI()):
    proclist = c.Win32_Process(name=EXE_NAME)
    if proclist:
        return proclist[0]
    else:
        return None


def _first_of(typ):
    def _inner(self):
        idxs = self.hw_indices[typ]
        if idxs:
            return self.hardware[idxs[0]]
        else:
            return None

    return _inner


class OHM:

    wohm = None  # a wmi.WMI instance
    connection_options = {
        'computer': '',
        'impersonation_level': '',
        'authentication_level': '',
        'authority': '',
        'privileges': '',
        'moniker': '',
        'suffix': '',
        'user': '',
        'password': '',
        'find_classes': False,
        'debug': False
    }
    hw_indices = dict((typ, ()) for typ in KNOWN_HW_TYPES)

    hardware = ()
    sensors = ()

    def __init__(self, **kwargs):
        self.connection_options = dict(
            [key, kwargs.get(key, self.connection_options[key])]
            for key in self.connection_options
        )

        self._init_wohm()
        self._init_hardware()

    def _init_wohm(self):
        self.wohm = wmi.WMI(namespace=NAMESPACE, **self.connection_options)
        return self.wohm

    def _init_hardware(self):
        self.hw_indices = OHM.hw_indices.copy()
        hardware = []
        sensors = []
        for typ in KNOWN_HW_TYPES:
            typ_indices = []
            for h in self.wohm.Hardware(HardwareType=typ):
                H = Hardware.find(self, InstanceId=h.InstanceId)
                idx = len(hardware)
                hardware.append(H)
                typ_indices.append(idx)

                sensors.extend(H.sensors)

            self.hw_indices[typ] = tuple(typ_indices)

        self.hardware = tuple(hardware)
        self.sensors = tuple(sensors)

    first_Mainboard = property(_first_of('Mainboard'))
    first_SuperIO = property(_first_of('SuperIO'))
    first_CPU = property(_first_of('CPU'))
    first_GpuNvidia = property(_first_of('GpuNvidia'))
    first_GpuAti = property(_first_of('GpuAti'))
    first_TBalancer = property(_first_of('Tbalancer'))
    first_Heatmaster = property(_first_of('Heatmaster'))
    first_HDD = property(_first_of('HDD'))
    first_RAM = property(_first_of('RAM'))

    @property
    def first_Gpu(self):
        idxs = self.hw_indices['GpuAti']
        if not idxs:
            idxs = self.hw_indices['GpuNvidia']
            if not idxs:
                return None
        return self.hardware[idxs[0]]


class Sensor(tuple):

    __slots__ = ()

    # ohm = property(itemgetter(0))
    SensorType = property(itemgetter(1))
    Identifier = property(itemgetter(2))
    InstanceId = property(itemgetter(3))
    Index = property(itemgetter(4))
    Name = property(itemgetter(5))
    Parent = property(itemgetter(6))

    def __new__(cls, ohm: OHM, s: wmi._wmi_object):
        assert hasattr(s, 'SensorType'), "Second argument of ohm.Sensor " \
                                         "constructor should be an " \
                                         "OpenHardwareMonitor wmi Sensor " \
                                         "object"

        return super().__new__(cls, (
            ohm, s.SensorType, s.Identifier, s.InstanceId, s.Index, s.Name,
            s.Parent
        ))

    @classmethod
    def find(cls, ohm: OHM, multiple=False, **selector):
        s = ohm.wohm.Sensor(**selector)
        if not s:
            raise NotFoundException(cls, selector)

        if multiple:
            return (Sensor(ohm, _s) for _s in s)
        else:
            if len(s) > 1:
                warnings.warn(MultipleFoundWarning(cls, selector))
            return Sensor(ohm, s[0])

    @classmethod
    def ofHardware(cls, ohm: OHM, h: wmi._wmi_object) -> 'Sensor iterator':
        for s in ohm.wohm.Sensor(Parent=h.Identifier):
            yield Sensor(ohm, s)

    @property
    def wmiSensor(self):
        return self._attr_query()

    @property
    def Value(self):
        return self._attr_query('Value').Value

    @property
    def Min(self):
        return self._attr_query('Min').Min

    @property
    def Max(self):
        return self._attr_query('Max').Max

    @property
    def units(self):
        return KNOWN_SENSOR_TYPE_UNITS[
                KNOWN_SENSOR_TYPES.index(self.SensorType)]

    def __repr__(self):
        return "<{qualname} SensorType={self[1]} Name={self[5]!r}" \
               " InstanceId={self[3]} Identifier={self[2]!r}>".format(
                    self=self, qualname=self.__class__.__qualname__
               )

    def _attr_query(self, *fields):
        q = self[0].wohm.Sensor(fields, Identifier=self.Identifier)
        if not q:
            raise WmiAttributeError(Sensor, fields)
        return q[0]


def generateSensorMap(sensors):
    mapp = {}
    for S in sensors:
        if S.SensorType not in mapp:
            mapp[S.SensorType] = {}

        mapp[S.SensorType][S.Index] = S

    return mapp


class Hardware(tuple):

    __slots__ = ()

    # ohm = property(itemgetter(0))
    HardwareType = property(itemgetter(1))
    Parent = property(itemgetter(2))
    InstanceId = property(itemgetter(3))
    Identifier = property(itemgetter(4))
    Name = property(itemgetter(5))
    sensors = property(itemgetter(6))
    # sensormap = property(itemgetter(7))

    def __new__(cls, ohm: OHM, h: wmi._wmi_object):
        assert hasattr(h, 'HardwareType'), "Second argument of ohm.Hardware" \
                                           " constructor should be an" \
                                           " OpenHardwareMonitor wmi" \
                                           " Hardware object"
        sensors = tuple(Sensor.ofHardware(ohm, h))
        sensormap = generateSensorMap(sensors)

        return super().__new__(cls, (
            ohm, h.HardwareType, h.Parent, h.InstanceId, h.Identifier, h.Name,
            sensors, sensormap
        ))

    @classmethod
    def find(cls, ohm: OHM, multiple=False, **selector):
        h = ohm.wohm.Hardware(**selector)
        if not h:
            raise NotFoundException(cls, selector)

        if multiple:
            return (Hardware(ohm, _h) for _h in h)
        else:
            if len(h) > 1:
                warnings.warn(MultipleFoundWarning(cls, selector))
            return Hardware(ohm, h[0])

    @property
    def wmiHardware(self):
        return self[0].wohm.Hardware(Identifier=self.Identifier)

    def __repr__(self):
        return "<{qualname} HardwareType={self[1]} Name={self[5]!r}" \
               " InstanceId={self[3]} Identifier={self[4]!r}" \
               " sensors={L}>".format(self=self, L=len(self[6]),
                                      qualname=self.__class__.__qualname__)

    def getSensor(self, sensortype, multiple=False):
        S = self[7].get(sensortype, {})
        if multiple:
            return S and S.copy()
        if not S:
            return S
        for k in S:
            # return first
            return S[k]
