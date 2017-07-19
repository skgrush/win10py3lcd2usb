"""Module for python interfaces to WMI, the Windows Management Interface."""

# ref: http://timgolden.me.uk/python/wmi/cookbook.html

from operator import itemgetter
import warnings
from collections import OrderedDict

import wmi


class WmiIfaceWarning(RuntimeWarning, UserWarning):
    """Base class for warnings raised in the module."""

    pass


class WmiIfaceException(RuntimeError):
    """An exception base class for wmi_interface exceptions."""

    pass


class NotFoundException(WmiIfaceException):
    """A WMI class instance was not found."""

    def __init__(self, typ, selectors):
        """Construct from a type not found by selectors."""
        self.type, self.selectors = typ, selectors
        self.message = "Failed to find {.__name__} with selectors {}".format(
            typ, selectors)
        super().__init__(self.message)


class MultipleFoundWarning(WmiIfaceWarning):
    """Too many WMI class instances were found."""

    def __init__(self, typ, selectors):
        """Construct from the type found by selectors."""
        self.type, self.selectors = typ, selectors
        self.message = "Found multiple {.__name__} with selectors {}".format(
            typ, selectors)
        super().__init__(self.message)


class WmiAttributeError(WmiIfaceException):
    """An error occurred retrieving an attribute from a WMI class."""

    def __init__(self, typ, attribute):
        """Construct from the type and attribute that failed."""
        self.type, self.attribute = typ, attribute
        self.message = "Failed to retrieve {.__name__} attribute(s) {}".format(
            typ, attribute)
        super().__init__(self.message)


def filterDict(inputDict: dict, searchKeys: 'container', retClass=OrderedDict):
    """Filter a dict-like object using a set of search keys.

    Arguments
    ---------
        inputDict: The dict-like object to be filtered. Must either implement
            `.items()`, or support iteration and the accessor method.
        searchKeys: Container of keys to filter by. Must be testable for
            membership, e.g. "a in b".
        returnClass: the class to return. Defaults to OrderedDict.
    """
    if hasattr(inputDict, 'items'):
        return retClass((k, v) for k, v in inputDict.items()
                        if k in searchKeys)

    return retClass((k, inputDict[k]) for k in inputDict
                    if k in searchKeys)


WNW_IDX_CONNOPTS = 0
WNW_IDX_CLASSES = 1


class WmiNamespaceWrapper(tuple):
    """Wrapper for WMI namespaces.

    Internal Components:
        self[0]: connection_options dictionary
        self[1]: class wrapper instances as an OrderedDict
    """

    __slots__ = ('wmiNS',)

    def __new__(cls, connection_options=()):
        """Construct a WmiNamespaceWrapper."""
        components = [None, None]
        # configure connection options
        conn_opts = cls.default_connection_options()
        conn_opts.update(connection_options)
        components[WNW_IDX_CONNOPTS] = conn_opts

        components[WNW_IDX_CLASSES] = OrderedDict(cls._classes())

        return super().__new__(cls, components)

    def __init__(self, connection_options):  # noqa W0231 super-init-not-called
        """Initialize WmiNamespaceWrapper."""
        self._init_wmiNS()
        self._init_classes()

    def _init_wmiNS(self):
        self.wmiNS = wmi.WMI(**self.connection_options)
        return self.wmiNS

    def _init_classes(self):
        """Initialize or refresh WmiClassWrapper instances."""
        classDict = self[WNW_IDX_CLASSES]
        for classname, dictVal in classDict.items():
            if not isinstance(dictVal, dict):
                # first init
                classDict[classname] = OrderedDict()
            else:
                for inst in classDict[classname].values():
                    inst._init_class()  # noqa W0212 protected-access

    @property
    def connection_options(self):
        """Property: Connection options for this instance."""
        return self[0].copy()

    @classmethod
    def default_connection_options(cls):
        """Return connection options for this namespace with inheritance."""
        connection_options = super()._default_connection_options()
        connection_options.update(cls._default_connection_options())
        connection_options.update()
        return connection_options

    @classmethod
    def _default_connection_options(cls):
        """Return connection options specific to this namespace as dictionary.

        Override this classmethod and return options that override these.
        """
        return {
            'namespace': '',
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

    @classmethod
    def _classes(cls) -> OrderedDict:
        """Return WMI classes in this namespace.

        Should be an ordered-dictionary mapping WMI class names to the
        appropriate WmiClassWrapper subclass.

        Override this classmethod and return classes in this namespace.
        """
        return OrderedDict()

    @classmethod
    def _defClassProp(cls, classname):
        """Define a property for handling calls to the given class name."""
        def _defClassProp_getter(self, **where_clause):
            results = []



WCW_IDX_PARENT = 0
WCW_IDX_SELECTORS = 1
WCW_IDX_STATATTRS = 2
WCW_LEN = 3


class WmiClassWrapper(tuple):
    """Wrapper for a known WMI class.

    Internal Components:
        self[0]: parent WmiNamespaceWrapper instance.
        self[2]: dictionary of selectors for the instance.
        self[3]: list of cached static attribute values.
    """

    __slots__ = ('wmiClass',)

    namespaceWrapper = property(itemgetter(WCW_IDX_PARENT), doc="Wrapper of"
                                " the parent WmiNamespaceWrapper of this"
                                " class.")

    @property
    def selectorsHash(self):
        """Hash of the selectors that selected this instance."""
        return hash(self[WCW_IDX_SELECTORS])

    @classmethod
    def static_attributes(cls):
        """Return iterable of names of static attributes for this class.

        Override this classmethod.
        """
        return ()

    @classmethod
    def dynamic_attributes(cls):
        """Return iterable of names of dynamic attributes for this class.

        Override this classmethod.
        """
        return ()

    def __new__(cls, namespace: WmiNamespaceWrapper, selectors):
        """Construct a WmiClassWrapper instance.

        Arguments:
            namespace: Should be a WmiNamespaceWrapper instance that this class
                exists in.
            selectors:
        """
        self_ = [None] * WCW_LEN
        # these components are static
        self_[WCW_IDX_PARENT] = namespace
        self_[WCW_IDX_SELECTORS] = filterDict(selectors,
                                              cls.static_attributes())

        # determined at __init__
        self_[WCW_IDX_STATATTRS] = [None] * len(cls.static_attributes())

        return super().__new__(cls, self_)

    def __init__(self, namespace, selectors):  # noqa W0231 super-init-not-call
        self._init_class()

    def _init_class(self):
        name = self._classname()
        wmiNS = self[WCW_IDX_PARENT].wmiNS
        wcls = getattr(wmiNS, name)
        wself = wcls(**self[WCW_IDX_SELECTORS])
        if len(wself) > 1:
            warnings.warn(MultipleFoundWarning(wcls, self[WCW_IDX_SELECTORS]))
        self.wmiClass = wself[0]

        self[WCW_IDX_STATATTRS][:] = \
            wmiNS.fetch_as_lists(name,
                                 self.static_attributes(),
                                 **self[WCW_IDX_SELECTORS]
                                )[0]  # noqa

    @staticmethod
    def _defStatAttr(idx: int):
        def __statAttrLookup(self):
            return self[WCW_IDX_STATATTRS][idx]
        return __statAttrLookup

    @staticmethod
    def _defDynAttr(attrName: str):
        def __wmiClass_getattr(self):
            return getattr(self.wmiClass, attrName)
        return __wmiClass_getattr

    @staticmethod
    def _defConstAttr(attrValue):
        def __returnConst(self):
            return attrValue
        return __returnConst

    @classmethod
    def _classname(cls):
        """Return WMI classname.

        Override this if needed, such as if the WMI classname is reserved
        in python. Defaults to this class's name.
        """
        return cls.__name__

    def _key(self):
        """Return a value to (unique-ish-ly) identify this instance.

        Override this if needed. Defaults to the hash of self's selectors.
        """
        return self.selectorsHash
