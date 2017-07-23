"""OpenHardwareMonitor interface through WMI."""

from collections import OrderedDict
from operator import itemgetter
import warnings

import wmi
from wmi import _wmi_object  # noqa

from wmi_interfaces import NotFoundException, MultipleFoundWarning, \
                           WmiAttributeError, \
                           WmiNamespaceWrapper, WmiClassWrapper

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


def get_process(cwmi: wmi.WMI=wmi.WMI()) -> "WMI().Win32_Process":
    """Get and return the process EXE_NAME."""
    proclist = cwmi.Win32_Process(name=EXE_NAME)
    if proclist:
        return proclist[0]


def wait_for_process(cwmi: wmi.WMI=wmi.WMI(),
                     timeout=None) -> "WMI().Win32_Process":
    """Wait until the process starts and return it."""
    watcher = cwmi.watch_for(notification_type="Creation",
                             wmi_class="Win32_Process",
                             Name=EXE_NAME)

    if not timeout or not hasattr(wmi, 'x_wmi_timed_out'):
        return watcher()
    else:
        try:
            return watcher(timeout)
        except wmi.x_wmi_timed_out:
            return None


def _first_of(typ):
    def _inner(self):
        idxs = self.hw_indices[typ]
        if idxs:
            return self.hardware[idxs[0]]

    return _inner


class Hardware(WmiClassWrapper):

    HardwareType = property(WmiClassWrapper._defStatAttr(0))
    ParentId = property(WmiClassWrapper._defStatAttr(1))
    Identifier = property(WmiClassWrapper._defStatAttr(2))
    Name = property(WmiClassWrapper._defStatAttr(3))
    InstanceId = property(WmiClassWrapper._defStatAttr(4))

    @property
    def ParentHardware(self):
        """Retrieve python Hardware instance referred to by self.ParentId."""
        return  # TODO

    @classmethod
    def static_attributes(cls):  # noqa
        return ('HardwareType', 'Parent', 'Identifier', 'Name', 'InstanceId')


class Sensor(WmiClassWrapper):

    SensorType = property(WmiClassWrapper._defStatAttr(0), doc="SensorType"
                          " [static string]. See KNOWN_SENSOR_TYPES"
                          " for possible values.")
    Name = property(WmiClassWrapper._defStatAttr(1), doc="Human-readable Name"
                    " [static string].")
    Identifier = property(WmiClassWrapper._defStatAttr(2), doc="Unique"
                          " path-like identifier [static string]. The OHM docs"
                          " warn that \"The identifiers are unique per"
                          " instance, but do not guarantee that the underlying"
                          " hardware is 100% identical to a previous session\""
                          ". This shouldn't be a problem during our runtime.")
    ParentId = property(WmiClassWrapper._defStatAttr(3), doc="Identifier of"
                        " the parent Hardware instance [static string].")
    Index = property(WmiClassWrapper._defStatAttr(4), doc="Index of this"
                     " sensor in its parent's array of this SensorType"
                     " [static int].")

    Value = property(WmiClassWrapper._defDynAttr('Value'), doc="Value of the"
                     " sensor [dynamic float].")
    Min = property(WmiClassWrapper._defDynAttr('Min'), doc="Lowest value read"
                   " from the sensor during this session [dynamic float]. This"
                   " may *increase* during our runtime if the OHM process is"
                   " restarted/reset.")
    Max = property(WmiClassWrapper._defDynAttr('Max'), doc="Highest value read"
                   " from the sensor during this session [dynamic float]."
                   " This may *decrease* during our runtime if the OHM process"
                   " is restarted/reset.")

    @property
    def ParentHardware(self):
        """Retrieve python Hardware instance referred to by self.ParentId."""
        return  # TODO

    @property
    def Units(self):
        try:
            return KNOWN_SENSOR_TYPE_UNITS[
                    KNOWN_SENSOR_TYPES.index(self.SensorType)]
        except AttributeError:
            return '??'

    @classmethod
    def static_attributes(cls): #noqa
        return ('SensorType', 'Name', 'Identifier', 'Parent', 'Index')

    @classmethod
    def dynamic_attributes(cls): #noqa
        return ('Value', 'Min', 'Max')


class OHM(WmiNamespaceWrapper):
    """Wrapper of bits of OpenHardwareMonitor's WMI interface.

    Subclasses:
        Hardware, root/OpenHardwareMonitor:Hardware
        Sensor, root/OpenHardwareMonitor:Sensor
    """

    @classmethod
    def _classes(cls):
        return OrderedDict((
            ('Hardware', Hardware),
            ('Sensor', Sensor),
        ))

    @classmethod
    def _default_connection_options(cls):
        return {
            'namespace': NAMESPACE
        }

    Hardware = property(WmiNamespaceWrapper._defClassProp('Hardware',
                                                          Hardware))
    Sensor = property(WmiNamespaceWrapper._defClassProp('Sensor', Sensor))



class OHM_old:
    """Wrapper of bits of OpenHardwareMonitor's WMI interface."""

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
        """Construct from given connection_options."""
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

    first_Mainboard = property(_first_of('Mainboard'), doc="Motherboard")
    first_SuperIO = property(_first_of('SuperIO'), doc="I/O Controller")
    first_CPU = property(_first_of('CPU'), doc="CPU")
    first_GpuNvidia = property(_first_of('GpuNvidia'), doc="GPU (Green)")
    first_GpuAti = property(_first_of('GpuAti'), doc="GPU (Red)")
    first_TBalancer = property(_first_of('Tbalancer'), doc="Pump controller")
    first_Heatmaster = property(_first_of('Heatmaster'), doc="??")
    first_HDD = property(_first_of('HDD'), doc="Storage")
    first_RAM = property(_first_of('RAM'), doc="Memory")

    @property
    def first_Gpu(self):
        """first_GpuAti[0] | first_Gpu_Nvidia[0]."""
        idxs = self.hw_indices['GpuAti']
        if not idxs:
            idxs = self.hw_indices['GpuNvidia']
            if not idxs:
                return None
        return self.hardware[idxs[0]]


class Sensor_old(tuple):
    """Wrapper of OHM's WMI Sensor class."""

    __slots__ = ()

    # ohm = property(itemgetter(0))
    SensorType = property(itemgetter(1))
    Identifier = property(itemgetter(2))
    InstanceId = property(itemgetter(3))
    Index = property(itemgetter(4))
    Name = property(itemgetter(5))
    Parent = property(itemgetter(6))

    def __new__(cls, ohm: OHM, s: _wmi_object):
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
    def ofHardware(cls, ohm: OHM, h: _wmi_object) -> 'Sensor iterator':
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
    """Map an iterator of Sensors based on sensor type and index."""
    mapp = {}
    for S in sensors:
        if S.SensorType not in mapp:
            mapp[S.SensorType] = {}

        mapp[S.SensorType][S.Index] = S

    return mapp


class Hardware_old(tuple):
    """Wrapper of OHM's WMI Hardware class."""

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
        """Attempt to retrieve sensor(s) of a given type for the hardware."""
        S = self[7].get(sensortype, {})
        if multiple:
            return S and S.copy()
        if not S:
            return S
        for k in S:
            # return first
            return S[k]
