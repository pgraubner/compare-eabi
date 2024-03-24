from arm_tags import Tags_Config

DEFAULT = '<DEFAULT>'

class AttributeTypes:
    TYPES = {"target-related": [4,5,6,7,8,9,10,11,12,48,36,34,66,68,42,44,46,50,52],
             "procedure-call": [13,14,15,16,17,18,26,24,25,19,20,21,22,23,38,27,28,29,72,74],
             "misc": [76],
             "optimization": [30,31],
             "compatibility": [32,65],
             "conformance": [67],
             "no-defaults": [64]}

    @staticmethod
    def all():
        return AttributeTypes.TYPES.keys()

    @staticmethod
    def is_attr_type(attr):
        return attr in AttributeTypes.TYPES

    @staticmethod
    def get_attr_type(tag_index):
        for key, val in AttributeTypes.TYPES.items():
            if tag_index in val:
                return key
        return None

class ArmAttributes:
    @staticmethod
    def is_valid(tag):
        return tag in Tags_Config

    @staticmethod
    def attr_names():
        return Tags_Config.keys()

    @staticmethod
    def get_attr_info(name):
        if Tags_Config[name][1] == "NTBS":
            return NtbsAttributeInfo(name)
        else:
            return NumericAttributeInfo(name)


class AttributeInfo:
    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return self._name

    def is_default(self, val):
        if val == DEFAULT:
            return True
        if val == self.get_default():
            return True
        return False

    def datatype(self):
        raise NotImplementedError()

    def is_string(self):
        raise NotImplementedError()

    def get_default(self):
        raise NotImplementedError()

    def attr_type(self):
        return AttributeTypes.get_attr_type(self.tag_index())

    def values(self):
        vals = Tags_Config[self._name][2]
        if isinstance(vals, dict):
            return vals.keys()
        return vals

    def tag_index(self):
        return Tags_Config[self._name][0]


class NtbsAttributeInfo(AttributeInfo):
    def __init__(self, name):
        super(NtbsAttributeInfo, self).__init__(name)

    def datatype(self):
        return "NTBS"

    def is_string(self):
        return True

    def get_default(self):
        return '""'


class NumericAttributeInfo(AttributeInfo):
    def __init__(self, name):
        super(NumericAttributeInfo, self).__init__(name)

    def datatype(self):
        return "uleb128"

    def is_string(self):
        return False

    def get_default(self):
        assert Tags_Config[self._name][2] is not None, "{}".format(self._name)
        vals = Tags_Config[self._name][2]
        if isinstance(vals, dict):
            return list(vals.values())[0]
        return vals[0]

    def index(self, val):
        assert Tags_Config[self._name][2] is not None, "{}".format(self._name)
        vals = Tags_Config[self._name][2]
        if val == DEFAULT:
            return 0
        if isinstance(vals, dict):
            return vals[val]
        return vals.index(val)

