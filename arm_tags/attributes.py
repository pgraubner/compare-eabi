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


class AttributeInfo:
    def __init__(self, name):
        self.__name = name

    def attr_type(self):
        return AttributeTypes.get_attr_type(self.tag_index())

    def datatype(self):
        return Tags_Config[self.__name][1]

    def is_string(self):
        return Tags_Config[self.__name][1] == "NTBS"

    def values(self):
        vals = Tags_Config[self.__name][2]
        if isinstance(vals, dict):
            return vals.keys()
        return vals

    def get_default(self):
        if self.is_string():
            return '""'
        assert Tags_Config[self.__name][2] is not None, "{}".format(self.__name)
        vals = Tags_Config[self.__name][2]
        if isinstance(vals, dict):
            return vals.values[0]
        return vals[0]

    def index(self, val):
        assert Tags_Config[self.__name][2] is not None, "{} {}".format(self.__name, val)
        vals = Tags_Config[self.__name][2]
        if val == DEFAULT:
            val = vals[0]
        if isinstance(vals, dict):
            return vals[val]
        return vals.index(val)

    def tag_index(self):
        return Tags_Config[self.__name][0]

class ArmAttributes:
    @staticmethod
    def is_valid(tag):
        return tag in Tags_Config

    @staticmethod
    def all():
        return Tags_Config.keys()

    @staticmethod
    def get_attr_info(name):
        return AttributeInfo(name)


