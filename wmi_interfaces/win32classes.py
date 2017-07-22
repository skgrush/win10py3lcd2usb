"""Module for a couple of WMI classes.

Reminder to self:
    DON'T fully map the classes. There's too much unneeded info there.
"""

from wmi_interfaces import WmiClassWrapper
import wmi  # noqa

# WMI().Win32_DiskDrive()
# https://msdn.microsoft.com/en-us/library/aa394132(v=vs.85).aspx

# WMI().Win32_BaseBoard()
# https://msdn.microsoft.com/en-us/library/aa389273(v=vs.85).aspx

# WMI().Win32_BIOS()
# https://msdn.microsoft.com/en-us/library/aa389273(v=vs.85).aspx

# WMI().Win32_PhysicalMemory()
# https://msdn.microsoft.com/en-us/library/aa394347(v=vs.85).aspx

# WMI().Win32_PhysicalMemoryArray()
# https://msdn.microsoft.com/en-us/library/aa394348(v=vs.85).aspx

# WMI().Win32_Processor()
# https://msdn.microsoft.com/en-us/library/aa394373(v=vs.85).aspx

# WMI().Win32_NetworkAdapter(PhysicalAdapter=True)
# https://msdn.microsoft.com/en-us/library/aa394216(v=vs.85).aspx

# WMI().Win32_NetworkAdapterConfiguration()
# https://msdn.microsoft.com/en-us/library/aa394217(v=vs.85).aspx

# WMI().Win32_VideoController()
#

# WMI().Win32_MotherboardDevice()

# WMI().Win32_MemoryDevice()


# Win32_TemperatureSensor

class Win32_OperatingSystem(WmiClassWrapper):
    """Wrapper for the Win32_OperatingSystem WMI class.

    "The Win32_OperatingSystem WMI class represents a Windows-based operating
    system installed on a computer." - Microsoft WMI Documentation

    References
    ----------
        This link will be dead soon.
        https://msdn.microsoft.com/en-us/library/aa394239(v=vs.85).aspx

    """

    @staticmethod
    def static_attributes():
        """See WmiClassWrapper.static_attributes."""
        return ('BootDevice', 'Caption', 'CSName', 'InstallDate',
                'LastBootUpTime', 'Locale', 'MaxNumberOfProcesses',
                'MaxProcessMemorySize', 'Name', 'SerialNumber', 'SuiteMask',
                'SystemDevice', 'SystemDirectory', 'SystemDrive',
                'TotalSwapSpaceSize', 'TotalVirtualMemorySize',
                'TotalVisibleMemorySize', 'Version', 'WindowsDirectory')

    @staticmethod
    def dynamic_attributes():
        """See WmiClassWrapper.dynamic_attributes."""
        return ('Description', 'FreePhysicalMemory', 'FreeSpaceInPagingFiles',
                'FreeVirtualMemory', 'NumberOfProcesses', 'NumberOfUsers',
                'RegisteredUser', 'SizeStoredInPagingFiles', 'Status')

    BootDevice = property(WmiClassWrapper._defStatAttr(0), doc="[string]")
    Caption = property(WmiClassWrapper._defStatAttr(3), doc="[string]")
    CSName = property(WmiClassWrapper._defStatAttr(9), doc="[string]")
    Description = property(WmiClassWrapper._defDynAttr('Description'),
                           doc="[string]")
    FreePhysicalMemory = property(
        WmiClassWrapper._defDynAttr('FreePhysicalMemory'), doc="[uint64]")
    FreeSpaceInPagingFiles = property(
        WmiClassWrapper._defDynAttr('FreeSpaceInPagingFiles'), doc="[uint64]")
    FreeVirtualMemory = property(
        WmiClassWrapper._defDynAttr('FreeVirtualMemory'), doc="[uint64]")
    InstallDate = property(WmiClassWrapper._defStatAttr(17), doc="[datetime]")
    LastBootUpTime = property(WmiClassWrapper._defStatAttr(19),
                              doc="[datetime]")
    MaxNumberOfProcesses = property(WmiClassWrapper._defStatAttr(22),
                                    doc="[uint32]")
    MaxProcessMemorySize = property(WmiClassWrapper._defStatAttr(23),
                                    doc="[uint64]")
    Name = property(WmiClassWrapper._defStatAttr(25), doc="[string]")
    NumberOfProcesses = property(
        WmiClassWrapper._defDynAttr('NumberOfProcesses'), doc="[uint32]")
    RegisteredUser = property(WmiClassWrapper._defDynAttr('RegisteredUser'),
                              doc="[string]")
    SerialNumber = property(WmiClassWrapper._defStatAttr(38), doc="[string]")
    SizeStoredInPagingFiles = property(
        WmiClassWrapper._defDynAttr('SizeStoredInPagingFiles'), doc="[uint64]")
    Status = property(WmiClassWrapper._defDynAttr('Status'), doc="[string]")
    SuiteMask = property(WmiClassWrapper._defStatAttr(41), doc="[uint32]")
    SystemDevice = property(WmiClassWrapper._defStatAttr(42), doc="[string]")
    SystemDirectory = property(WmiClassWrapper._defStatAttr(43),
                               doc="[string]")
    SystemDrive = property(WmiClassWrapper._defStatAttr(44), doc="[string]")
    TotalSwapSpaceSize = property(WmiClassWrapper._defStatAttr(45),
                                  doc="[uint64]")
    TotalVirtualMemorySize = property(WmiClassWrapper._defStatAttr(46),
                                      doc="[uint64]")
    TotalVisibleMemorySize = property(WmiClassWrapper._defStatAttr(47),
                                      doc="[uint64]")
    Version = property(WmiClassWrapper._defStatAttr(48), doc="[string]")
    WindowsDirectory = property(WmiClassWrapper._defStatAttr(49),
                                doc="[string]")
