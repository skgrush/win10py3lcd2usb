"""Overcomplicated stuff that shouldn't be used.

I spent hours making this silly class before deciding it was a bad idea. But I
spent too long on it to just delete it.
"""

from wmi_interfaces import WmiClassWrapper


class Win32_OperatingSystem(WmiClassWrapper):
    """Wrapper for the Win32_OperatingSystem WMI class.

    "The Win32_OperatingSystem WMI class represents a Windows-based operating
    system installed on a computer." - Microsoft WMI Documentation
    """

    @staticmethod
    def static_attributes():
        """See WmiClassWrapper.static_attributes."""
        return ('BootDevice', 'BuildNumber', 'BuildType', 'Caption', 'CodeSet',
                'CountryCode', 'CreationClassName', 'CSCreationClassName',
                'CSDVersion', 'CSName', 'CurrentTimeZone',
                'DataExecutionPrevention_Available',
                'DataExecutionPrevention_32BitApplications',  # 12
                'DataExecutionPrevention_Drivers',
                'DataExecutionPrevention_SupportPolicy', 'Debug',  # 15
                'Distributed', 'InstallDate', 'LargeSystemCache',  # 18
                'LastBootUpTime', 'Locale', 'Manufacturer',  # 21
                'MaxNumberOfProcesses', 'MaxProcessMemorySize',  # 23
                'MUILanguages', 'Name', 'OperatingSystemSKU',  # 26
                'OSArchitecture', 'OSLanguage', 'OSProductSuite',  # 29
                'OSType', 'OtherTypeDescription', 'PAEEnabled',  # 32
                'PlusProductID', 'PlusVersionNumber',  # 34
                'PortableOperatingSystem', 'Primary', 'ProductType',  # 37
                'SerialNumber', 'ServicePackMajorVersion',  # 39
                'ServicePackMinorVersion', 'SuiteMask', 'SystemDevice',  # 42
                'SystemDirectory', 'SystemDrive', 'TotalSwapSpaceSize',  # 45
                'TotalVirtualMemorySize', 'TotalVisibleMemorySize',  # 47
                'Version', 'WindowsDirectory', 'QuantumType')  # 50

    @staticmethod
    def dynamic_attributes():
        """See WmiClassWrapper.dynamic_attributes."""
        return ('Description', 'EncryptionLevel',
                'FreePhysicalMemory', 'FreeSpaceInPagingFiles',
                'FreeVirtualMemory', 'LocalDateTime',
                'NumberOfLicensedUsers', 'NumberOfProcesses',
                'NumberOfUsers', 'Organization', 'RegisteredUser',
                'SizeStoredInPagingFiles', 'Status', 'QuantumLength')

    BootDevice = property(WmiClassWrapper._defStatAttr(0), doc="[string]")
    BuildNumber = property(WmiClassWrapper._defStatAttr(1), doc="[string]")
    BuildType = property(WmiClassWrapper._defStatAttr(2), doc="[string]")
    Caption = property(WmiClassWrapper._defStatAttr(3), doc="[string]")
    CodeSet = property(WmiClassWrapper._defStatAttr(4), doc="[string]")
    CountryCode = property(WmiClassWrapper._defStatAttr(5), doc="[string]")
    CreationClassName = property(WmiClassWrapper._defStatAttr(6),
                                 doc="[string]")
    CSCreationClassName = property(WmiClassWrapper._defStatAttr(7),
                                   doc="[string]")
    CSDVersion = property(WmiClassWrapper._defStatAttr(8), doc="[string]")
    CSName = property(WmiClassWrapper._defStatAttr(9), doc="[string]")
    CurrentTimeZone = property(WmiClassWrapper._defStatAttr(10),
                               doc="[sint16]")
    DataExecutionPrevention_Available = property(
        WmiClassWrapper._defStatAttr(11), doc="[boolean]")
    DataExecutionPrevention_32BitApplications = property(
        WmiClassWrapper._defStatAttr(12), doc="[boolean]")
    DataExecutionPrevention_Drivers = property(
        WmiClassWrapper._defStatAttr(13), doc="[boolean]")
    DataExecutionPrevention_SupportPolicy = property(
        WmiClassWrapper._defStatAttr(14), doc="[uint8]")
    Debug = property(WmiClassWrapper._defStatAttr(15), doc="[boolean]")
    Description = property(WmiClassWrapper._defDynAttr('Description'),
                           doc="[string]")
    Distributed = property(WmiClassWrapper._defStatAttr(16), doc="[boolean]")
    EncryptionLevel = property(WmiClassWrapper._defDynAttr('EncryptionLevel'),
                               doc="[uint32]")
    ForegroundApplicationBoost = property(WmiClassWrapper._defConstAttr(2),
                                          doc="[uint8] = 2")
    FreePhysicalMemory = property(
        WmiClassWrapper._defDynAttr('FreePhysicalMemory'), doc="[uint64]")
    FreeSpaceInPagingFiles = property(
        WmiClassWrapper._defDynAttr('FreeSpaceInPagingFiles'), doc="[uint64]")
    FreeVirtualMemory = property(
        WmiClassWrapper._defDynAttr('FreeVirtualMemory'), doc="[uint64]")
    InstallDate = property(WmiClassWrapper._defStatAttr(17), doc="[datetime]")
    LargeSystemCache = property(WmiClassWrapper._defStatAttr(18),
                                doc="[uint32]")
    LastBootUpTime = property(WmiClassWrapper._defStatAttr(19),
                              doc="[datetime]")
    LocalDateTime = property(WmiClassWrapper._defDynAttr('LocalDateTime'),
                             doc="[datetime]")
    Locale = property(WmiClassWrapper._defStatAttr(20), doc="[string]")
    Manufacturer = property(WmiClassWrapper._defStatAttr(21), doc="[string]")
    MaxNumberOfProcesses = property(WmiClassWrapper._defStatAttr(22),
                                    doc="[uint32]")
    MaxProcessMemorySize = property(WmiClassWrapper._defStatAttr(23),
                                    doc="[uint64]")
    MUILanguages = property(WmiClassWrapper._defStatAttr(24), doc="[string[]]")
    Name = property(WmiClassWrapper._defStatAttr(25), doc="[string]")
    NumberOfLicensedUsers = property(
        WmiClassWrapper._defDynAttr('NumberOfLicensedUsers'), doc="[uint32]")
    NumberOfProcesses = property(
        WmiClassWrapper._defDynAttr('NumberOfProcesses'), doc="[uint32]")
    NumberOfUsers = property(WmiClassWrapper._defDynAttr('NumberOfUsers'),
                             doc="[uint32]")
    OperatingSystemSKU = property(WmiClassWrapper._defStatAttr(26),
                                  doc="[uint32]")
    Organization = property(WmiClassWrapper._defDynAttr('Organization'),
                            doc="[string]")
    OSArchitecture = property(WmiClassWrapper._defStatAttr(27), doc="[string]")
    OSLanguage = property(WmiClassWrapper._defStatAttr(28), doc="[uint32]")
    OSProductSuite = property(WmiClassWrapper._defStatAttr(29), doc="[uint32]")
    OSType = property(WmiClassWrapper._defStatAttr(30), doc="[uint16]")
    OtherTypeDescription = property(WmiClassWrapper._defStatAttr(31),
                                    doc="[string]")
    PAEEnabled = property(WmiClassWrapper._defStatAttr(32), doc="[Boolean]")
    PlusProductID = property(WmiClassWrapper._defStatAttr(33), doc="[string]")
    PlusVersionNumber = property(WmiClassWrapper._defStatAttr(34),
                                 doc="[string]")
    PortableOperatingSystem = property(WmiClassWrapper._defStatAttr(35),
                                       doc="[boolean]")
    Primary = property(WmiClassWrapper._defStatAttr(36), doc="[boolean]")
    ProductType = property(WmiClassWrapper._defStatAttr(37), doc="[uint32]")
    RegisteredUser = property(WmiClassWrapper._defDynAttr('RegisteredUser'),
                              doc="[string]")
    SerialNumber = property(WmiClassWrapper._defStatAttr(38), doc="[string]")
    ServicePackMajorVersion = property(WmiClassWrapper._defStatAttr(39),
                                       doc="[uint16]")
    ServicePackMinorVersion = property(WmiClassWrapper._defStatAttr(40),
                                       doc="[uint16]")
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
    QuantumLength = property(WmiClassWrapper._defDynAttr('QuantumLength'),
                             doc="[uint8]")
    QuantumType = property(WmiClassWrapper._defStatAttr(50), doc="[uint8]")
