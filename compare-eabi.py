#!/usr/bin/python3

import subprocess
import io
import shutil
import sys
import os
import argparse

from arm_eabi_diagnostics import Diagnostics
from arm_tags import Attributes, AttributeTypes, DEFAULT

class Colors:
    """"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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

class ObjFilelist:
    def __init__(self) -> None:
        self.__objfiles = []

    @staticmethod
    def from_array(arr):
        result = ObjFilelist()
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
        for tag in Attributes.get_all():
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

def write_tag_verbose(result, tag, val):
    result.write(Colors.HEADER)
    write_tag(result, tag, val)
    result.write(Colors.ENDC)
    result.write(Diagnostics[tag])
    result.write("\n")

def write_tag(result, tag, val):
    tag_info = Attributes.get_attr_info(tag)
    fmt = "| {:<30} | {:<50} | {:>5} | {:<7} |"
    if tag_info.is_string():
        if val == DEFAULT:
            val = "{} (Default)".format(tag_info.get_default())

        result.write(fmt.format(tag, val, "", tag_info.datatype()))
    else:
        if val == DEFAULT:
            val = "{} (Default)".format(tag_info.get_default())
            num = 0
        else:
            num = tag_info.index(val)
        result.write(fmt.format(tag, val, "{:#x}".format(num), tag_info.datatype()))

    result.write("\n")

def write_attr_type_header(result, attr_type):
    header = "{} attribute types".format(attr_type)
    result.write(Colors.HEADER)
    result.write(header)
    result.write("\n" + "-" * len(header))
    result.write("\n")
    result.write(Colors.ENDC)

class Diff:
    DIFF_PROPERTIES = {
                	#'identical': {'header': 'Identical tags\n', 'color': Colors.OKGREEN},
                    #'identical-or-default': {'header': 'Identical tags with default values\n', 'color': Colors.WARNING},
                    'non-identical': {'header': 'Tags with non-identical values (possibly conflicting)\n', 'color': Colors.FAIL}
                    }

    def __init__(self, attrs) -> None:
        self.__attrs = attrs
        self.__read_attrs()

    def __read_attrs(self):
        self.__properties = {}
        for p in Diff.DIFF_PROPERTIES:
            self.__properties[p] = []

        for attr, val in self.__attrs.items():
            if all_equal(val.values()):
                if all_default(val.values()):
                    continue
                #self.__properties['identical'].append(attr)
            elif all_equal_or_default(val.values()):
                #self.__properties['identical-or-default'].append(attr)
                self.__properties['non-identical'].append(attr)
            else:
                self.__properties['non-identical'].append(attr)


    def __repr__(self) -> str:
        result = io.StringIO()

        def write_property(key):
            prop = Diff.DIFF_PROPERTIES[key]
            result.write(Colors.BOLD)
            result.write(prop['header'])
            result.write("-" * len(prop['header']))
            result.write("\n")
            result.write(Colors.ENDC)

            for attr_type in AttributeTypes.all():
                write_attr_type_header(result, attr_type)

                for tag in self.__properties[key]:
                    info = Attributes.get_attr_info(tag)
                    if info.attr_type() != attr_type:
                        continue
                    result.write(prop['color'])
                    attr_dict = self.__attrs[tag]

                    for fn, val in attr_dict.items():
                        result.write("| {:<20} ".format( os.path.basename(fn)) )
                        write_tag(result, tag, val)

                    result.write(Colors.ENDC)
                    if verbose:
                        result.write(Diagnostics[tag])
                    result.write("\n")

        for p in Diff.DIFF_PROPERTIES:
            write_property(p)

        return result.getvalue()


class ArchiveFile:
    def __init__(self, fn) -> None:
        self.__fn = fn
        self.__objfiles = ObjFilelist()

    def is_archive(self):
        return True

    def objfiles(self):
        return self.__objfiles.objfiles()

    def collect(self):
        attrs = {}
        for tag in Attributes.get_all():
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
    def from_file(filename):
        out = subprocess.run([readelf, "-A", filename], stdout=subprocess.PIPE)
        buf = io.StringIO(out.stdout.decode('utf-8'))

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

        result.__objfiles = ObjFilelist.from_array(arr)
        return result

    def __repr__(self) -> str:
        return repr(self.__objfiles)

    def filename(self):
        return self.__fn


class ObjFile:
    def __init__(self, fn, attrs) -> None:
        self.__fn = fn
        self.__attrs = attrs

    def is_archive(self):
        return False

    def attrs(self):
        return self.__attrs

    def filter_by_attr_type(self, attr_type):
        result = {}
        for attr, val in self.__attrs.items():
            info = Attributes.get_attr_info(attr)
            if info.attr_type() == attr_type:
                result[attr] = val
        return result

    @staticmethod
    def from_objfile(filename):
        out = subprocess.run([readelf, "-A", filename], stdout=subprocess.PIPE)
        buf = io.StringIO(out.stdout.decode('utf-8'))
        return ObjFile.from_buf(filename, buf)

    @staticmethod
    def from_txtfile(filename):
        out = open(filename, "r").read()
        buf = io.StringIO(out)
        return ObjFile.from_buf(filename, buf)

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
                info = Attributes.get_attr_info(key)
                if info.attr_type() in filter:
                    attrs[key] = value

        result = ObjFile(filename, attrs)
        return result

    def __repr__(self) -> str:
        result = io.StringIO()

        result.write(Colors.BOLD)
        result.write(self.filename())
        result.write(Colors.ENDC)
        result.write("\n")

        for attr_type in AttributeTypes.all():
            items = self.filter_by_attr_type(attr_type).items()
            if len(items) == 0:
                continue

            write_attr_type_header(result, attr_type)

            for attr, val in items:
                if verbose:
                    write_tag_verbose(result, attr, val)
                else:
                    write_tag(result, attr, val)
            result.write("\n")

        return result.getvalue()

    def filename(self):
        return self.__fn

def diff(objfiles):
    objs = ObjFilelist.from_array(objfiles)
    print(objs.compare())

def details(objfiles):
    for o in objfiles:
        print(o)

def explain(tag):
    if tag not in Attributes.get_all():
        print("Error: {} not a valid tag".format(tag))
        sys.exit(1)
    if tag not in Diagnostics:
        print("Error: {} has no diagnostics information".format(tag))
        sys.exit(1)
    print(Colors.BOLD, tag, Colors.ENDC)
    print(Diagnostics[tag])


readelf = "readelf"
verbose = False
filter = AttributeTypes.all()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog='eabi-helper',
                        description='helps interpreting objects file in ARM32 ABI')
    parser.add_argument('--filter', nargs='+')
    parser.add_argument('--textfiles', nargs='+')
    parser.add_argument('--objfiles', nargs='+')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--diff', action='store_true')
    parser.add_argument('--readelf', nargs=1)
    parser.add_argument('--explain', action='store', type=str)

    args = parser.parse_args()

    if args.explain is not None:
        explain(args.explain)
    if args.readelf is not None:
        readelf = args.readelf[0]

    verbose = args.verbose

    path = shutil.which(readelf)
    if path is None:
        print("Error: {} not found".format(readelf))
        sys.exit(1)

    if args.filter is not None:
        filter = []
        for f in args.filter:
            if not AttributeTypes.is_attr_type(f):
                print("Error: unknown attribute {}".format(f))
                sys.exit(1)
            filter.append(f)


    objfiles = []
    if args.textfiles is not None:
        for o in args.textfiles:
            if not os.path.exists(o):
                print("Error: {} not found".format(o))
                sys.exit(1)
            objfiles.append(ObjFile.from_txtfile(o))

    if args.objfiles is not None:
        for o in args.objfiles:
            if not os.path.exists(o):
                print("Error: {} not found".format(o))
                sys.exit(1)

            if o.endswith(".a") or o.endswith(".rlib"):
                objfiles.append(ArchiveFile.from_file(o))
            else:
                objfiles.append(ObjFile.from_objfile(o))

    if len(objfiles) == 0:
        print("Error: nothing to do")
        sys.exit(1)

    if args.diff:
        diff(objfiles)
    else:
        details(objfiles)
