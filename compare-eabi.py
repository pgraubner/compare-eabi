#!/usr/bin/python3

import io
import shutil
import sys
import os
import argparse
import subprocess

from arm_eabi_diagnostics import ArmAttributesDiagnostics
from arm_tags.attributes import ArmAttributes, AttributeTypes, DEFAULT
from arm_tags.objfiles import ArchiveFile, Diff, ObjFileList, ObjFile

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

def print_objfile(objfile) -> str:
    result = io.StringIO()

    result.write(Colors.BOLD)
    result.write(objfile.filename())
    result.write(Colors.ENDC)
    result.write("\n")

    for attr_type in AttributeTypes.all():
        filtered_objfile = objfile.filter_by_attr_type(attr_type).attrs()
        if len(filtered_objfile) == 0:
            continue

        write_attr_type_header(result, attr_type)

        for tag, val in filtered_objfile.items():
            tag_info = ArmAttributes.get_attr_info(tag)
            if VERBOSE:
                write_tag_verbose(result, tag_info, val)
            else:
                write_tag(result, tag_info, val)
        result.write("\n")

    return result.getvalue()

DIFF_DISPLAY = {
                'identical': {'header': 'Identical tags\n', 'color': Colors.OKGREEN},
                #'identical-or-default': {'header': 'Identical tags with default values\n'},
                'non-identical': {'header': 'Tags with non-identical values (possibly conflicting)\n', 'color': Colors.FAIL}
                }

def print_diff(diff) -> str:
    result = io.StringIO()

    def write_property(key):
        prop = DIFF_DISPLAY[key]

        prop_header = True

        for attr_type in AttributeTypes.all():
            attr_header = True

            for tag in diff.properties(key):
                tag_info = ArmAttributes.get_attr_info(tag)
                if tag_info.attr_type() != attr_type:
                    continue
                attr_dict = diff.attrs(tag)
                if prop_header:
                    result.write(Colors.BOLD)
                    result.write(prop['header'])
                    result.write("-" * len(prop['header']))
                    result.write("\n")
                    result.write(Colors.ENDC)
                    prop_header = False

                if attr_header:
                    write_attr_type_header(result, attr_type)
                    attr_header = False

                result.write(prop['color'])
                result.write("{}\n".format(repr(tag_info)))
                for val in attr_dict.keys():
                    write_tag_diff(result, attr_dict[val], tag_info, val)

                result.write(Colors.ENDC)
                if VERBOSE:
                    result.write(ArmAttributesDiagnostics.diagnostics(tag))
                result.write("\n")

    for p in Diff.DIFF_PROPERTIES:
        write_property(p)

    return result.getvalue()


def write_tag_verbose(result, tag, val):
    result.write(Colors.HEADER)
    write_tag(result, tag, val)
    result.write(Colors.ENDC)
    result.write(ArmAttributesDiagnostics.diagnostics(tag))
    result.write("\n")

def repr_value(tag_info, val):
    if val == DEFAULT:
        return "{} (Default)".format(tag_info.get_default())
    return val

def write_tag(result, tag_info, val):
    fmt = "| {:<30} | {:<50} | {:>5} | {:<7} |"
    if tag_info.is_string():
        num = ""
    else:
        num = "{:#x}".format(tag_info.index(val))
    result.write(fmt.format(repr(tag_info), repr_value(tag_info, val), num, tag_info.datatype()))
    result.write("\n")

def repr_filenames(files):
    fns = [os.path.basename(fn.filename()) for fn in files]
    result = ", ".join(fns)
    num_fns = 3
    while len(result) > 60 and num_fns >= 1:
        result = ", ".join(fns[:num_fns]) + ",... ({} more files)".format(len(fns)-num_fns)
        num_fns -= 1
    if num_fns == 0:
        result = "..." + fns[0][-25:] + ",... ({} more files)".format(len(fns)-1)
    return result

def write_tag_diff(result, fns, tag_info, val):
    #result.write("| {:<20} ".format( os.path.basename(fns.filename()) ) )
    fmt = "| {:<30} | {:>5} | {:<7} | {:<50} |"
    if tag_info.is_string():
        num = ""
    else:
        num = "{:#x}".format(tag_info.index(val))
    result.write(fmt.format(repr_value(tag_info, val), num, tag_info.datatype(), repr_filenames(fns)))
    result.write("\n")


def write_attr_type_header(result, attr_type):
    header = "{} attribute types".format(attr_type)
    result.write(Colors.HEADER)
    result.write(header)
    result.write("\n" + "-" * len(header))
    result.write("\n")
    result.write(Colors.ENDC)

def read_objfile(filename):
    out = subprocess.run([READELF, "-A", filename], stdout=subprocess.PIPE)
    buf = io.StringIO(out.stdout.decode('utf-8'))
    return ObjFile.from_buf(filename, buf)

def read_txtfile(filename):
    out = open(filename, "r").read()
    buf = io.StringIO(out)
    return ObjFile.from_buf(filename, buf)

def read_archive(filename):
    out = subprocess.run([READELF, "-A", filename], stdout=subprocess.PIPE)
    buf = io.StringIO(out.stdout.decode('utf-8'))
    return ArchiveFile.from_buf(filename, buf)

def diff(objfiles):
    objs = ObjFileList.from_array(objfiles).filter_by_attr_type(*FILTER)
    print(print_diff(objs.compare()))

def details(objfiles):
    for o in objfiles:
        print(print_objfile(o.filter_by_attr_type(*FILTER)))

def explain(tag):
    if not ArmAttributes.is_valid(tag):
        print("Error: {} not a valid Arm Attribute".format(tag))
        sys.exit(1)
    if not ArmAttributesDiagnostics.has_diagnostics(tag):
        print("Error: {} has no diagnostics information".format(tag))
        sys.exit(1)
    print(Colors.BOLD, tag, Colors.ENDC)
    print(ArmAttributesDiagnostics.diagnostics(tag))

READELF = "readelf"
VERBOSE = False
FILTER = AttributeTypes.all()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog='compare-eabi',
                        description='compare-eabi helps interpreting ARM Attributes in objects file for the ARM32 ABI')
    parser.add_argument('--readelf', nargs=1, help="path to a ARM compliant readelf binutils tool")
    parser.add_argument('--textfiles', nargs='+', help="parse text files previously created with 'readelf -A <objfile>'")
    parser.add_argument('--objfiles', nargs='+', help="parse object files and archives by calling 'readelf -A <objfile>'")
    parser.add_argument('--filter', nargs='+', help="filters for attribute types. valid types are \"{}\"".format("\", \"".join(AttributeTypes.all())))
    parser.add_argument('--diff', action='store_true', help="compare ARM attributes for all listed text files, object files, and archives")
    parser.add_argument('--verbose', action='store_true', help="shows an explanation for each listed ARM attribute")
    parser.add_argument('--explain', action='store', type=str, help="shows an explanation for a particular ARM attribute")

    args = parser.parse_args()

    if args.explain is not None:
        explain(args.explain)
        sys.exit(0)
    if args.readelf is not None:
        READELF = args.readelf[0]

    VERBOSE = args.verbose

    path = shutil.which(READELF)
    if path is None:
        print("Error: {} not found".format(READELF))
        sys.exit(1)

    if args.filter is not None:
        FILTER = []
        for f in args.filter:
            if not AttributeTypes.is_attr_type(f):
                print("Error: unknown attribute {}".format(f))
                sys.exit(1)
            FILTER.append(f)


    objfiles = []
    if args.textfiles is not None:
        for o in args.textfiles:
            if not os.path.exists(o):
                print("Error: {} not found".format(o))
                sys.exit(1)
            objfiles.append(read_txtfile(o))

    if args.objfiles is not None:
        for o in args.objfiles:
            if not os.path.exists(o):
                print("Error: {} not found".format(o))
                sys.exit(1)

            if o.endswith(".a") or o.endswith(".rlib"):
                objfiles += read_archive(o).objfiles()
            else:
                objfiles.append(read_objfile(o))

    if len(objfiles) == 0:
        print("Error: nothing to do")
        sys.exit(1)

    if args.diff:
        diff(objfiles)
    else:
        details(objfiles)
