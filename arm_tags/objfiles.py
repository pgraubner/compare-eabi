
from arm_tags.attributes import DEFAULT, Attributes

class ObjFileList:
    """
    ObjFileList is a wrapper around a list of ObjFiles
    """
    def __init__(self) -> None:
        self.__objfiles = []

    def __iter__(self):
        return self.__objfiles.__iter__()

    def __next__(self):
        return self.__objfiles.__next__()

    def filter_by_attr_type(self, *attr_type):
        result = []
        for o in self.__objfiles:
            result.append(o.filter_by_attr_type(*attr_type))
        return ObjFileList.from_array(result)

    @staticmethod
    def from_array(arr):
        result = ObjFileList()
        result.__objfiles = arr

        return result

    def objfiles(self):
        return self.__objfiles

    def compare(self):
        objs = []
        for o in self.__objfiles:
            if o.is_archive():
                objs.append(o.collect())
                #objs += o.objfiles()
            else:
                objs.append(o)

        attrs = {}
        for tag in Attributes.all():
            attrs[tag] = {}
            for obj in objs:
                val = DEFAULT
                if tag in obj.attrs():
                    val = obj.attrs()[tag]
                attrs[tag][obj.filename()] = val

        result = Diff(attrs)
        return result

    def __repr__(self) -> str:
        return repr(self.__objfiles)

class ArchiveFile:
    def __init__(self, fn) -> None:
        self.__fn = fn
        self.__objfiles = ObjFileList()

    def is_archive(self):
        return True

    def objfiles(self):
        return self.__objfiles.objfiles()

    def collect(self):
        attrs = {}
        for tag in Attributes.all():
            val = None
            for obj in self.__objfiles.objfiles():
                if tag in obj.attrs():
                    if val is None:
                        val = obj.attrs()[tag]
                    else:
                        assert val == obj.attrs()[tag]
                    break
            if val is not None:
                attrs[tag] = val

        result = ObjFile(self.__fn, attrs)
        return result

    @staticmethod
    def from_buf(filename, buf):
        result = ArchiveFile(filename)
        arr = []

        while not buf.closed:
            line = buf.readline()
            if line == "\n":
                continue
            if line == "":
                break
            _, fn = line.split(":")
            arr.append(ObjFile.from_buf(fn, buf))

        result.__objfiles = ObjFileList.from_array(arr)
        return result

    def filename(self):
        return self.__fn

    def __repr__(self) -> str:
        return repr(self.__objfiles)


class ObjFile:
    def __init__(self, fn, attrs) -> None:
        self.__fn = fn
        self.__attrs = attrs

    def is_archive(self):
        return False

    def attrs(self):
        return self.__attrs

    def filter_by_attr_type(self, *attr_type):
        result = {}
        for attr in Attributes.all():
            if attr not in self.__attrs:
                continue
            val = self.__attrs[attr]
            info = Attributes.get_attr_info(attr)
            if info.attr_type() in attr_type:
                result[attr] = val
        return ObjFile(self.__fn, result)

    @staticmethod
    def from_buf(filename, buf):
        attrs = {}
        section_name = ""

        state = 'SECTION'
        while not buf.closed:
            line = buf.readline()
            if line == "\n" or line == "":
                break

            if state == 'SECTION':
                _, section_name = line.split(":")
                section_name = section_name.strip()
                state = 'ATTRIBUTES'
                continue

            if state == 'ATTRIBUTES':
                if line == "File Attributes\n":
                    continue
                key, value = line.split(":")
                value = value.strip()
                key = key.strip()

                # add attribute
                attrs[key] = value

        result = ObjFile(filename, attrs)
        return result

    def filename(self):
        return self.__fn

    def __repr__(self) -> str:
        return "{}: {}".format(self.__fn, self.__attrs)

class Diff:
    DIFF_PROPERTIES = ['identical',
                    #'identical-or-default',
                    'non-identical']

    def __init__(self, attrs) -> None:
        # TODO: use objfiles instead of attrs here
        self.__attrs = attrs
        self.__read_attrs()

    def properties(self, key):
        return self.__properties[key]

    def attrs(self, key):
        return self.__attrs[key]

    def __read_attrs(self):
        self.__properties = {}
        for p in Diff.DIFF_PROPERTIES:
            self.__properties[p] = []

        for attr, val in self.__attrs.items():
            if all_equal(val.values()):
                if all_default(val.values()):
                    continue
                self.__properties['identical'].append(attr)
            elif all_equal_or_default(val.values()):
                #self.__properties['identical-or-default'].append(attr)
                self.__properties['non-identical'].append(attr)
            else:
                self.__properties['non-identical'].append(attr)

    def __repr__(self) -> str:
        return "{}".format(self.__properties)

def all_equal(elements):
    if len(elements) == 0:
        return True
    first = None
    for item in elements:
        if first == None:
            first = item
            continue
        if item != first:
            return False
    return True

def all_equal_or_default(elements):
    first = DEFAULT
    for item in elements:
        if item == DEFAULT:
            continue
        if item != first:
            if first != DEFAULT:
                return False
            first = item

    return True

def all_default(elements):
    return all(x == DEFAULT for x in elements)

