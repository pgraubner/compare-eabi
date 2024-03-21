#!/usr/bin/python3

import shutil
import sys
import os
import argparse
import tempfile
import subprocess

ld = "ld"
ldflags = ""
ldstaticlibs = ""

def link(objfiles):
    with tempfile.TemporaryDirectory() as tmpdirname:
        files = [obj.filename() for obj in objfiles]
        elffile = "{}/test.elf".format(tmpdirname)
        flags = ldflags.split(" ") if ldflags != "" else []
        staticlibs = ldstaticlibs.split(" ") if ldstaticlibs != "" else []
        out = subprocess.run([ld, "-o", elffile, *flags, *files, *staticlibs], stdout=subprocess.PIPE)
        out = subprocess.run([readelf, "-A", filename], stdout=subprocess.PIPE)
        print(out.stdout.decode('utf-8'))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                        prog='test-linker',
                        description='helps interpreting objects file in ARM32 ABI')
    parser.add_argument('--objfiles', nargs='+')
    parser.add_argument('--link', action='store_true')
    parser.add_argument('--readelf', nargs=1)
    parser.add_argument('--ld', nargs=1)
    parser.add_argument('--ldflags', nargs=1)
    parser.add_argument('--ldstaticlibs', nargs=1)

    args = parser.parse_args()

    if args.explain is not None:
        if args.explain not in Tags.get_tags():
            print("Error: {} not a valid tag".format(args.explain))
            sys.exit(1)
        if args.explain not in Diagnostics:
            print("Error: {} has no diagnostics information".format(args.explain))
            sys.exit(1)
        print(Colors.BOLD, args.explain, Colors.ENDC)
        print(Diagnostics[args.explain])

    if args.readelf is not None:
        readelf = args.readelf[0]
    if args.ld is not None:
        ld = args.ld[0]
    if args.ldflags is not None:
        ldflags = args.ldflags[0]
    if args.ldstaticlibs is not None:
        ldstaticlibs = args.ldstaticlibs[0]

    verbose = args.verbose

    path = shutil.which(readelf)
    if path is None:
        print("Error: {} not found".format(readelf))
        sys.exit(1)
    path = shutil.which(ld)
    if path is None:
        print("Error: {} not found".format(ld))
        sys.exit(1)

    if args.objfiles is not None:
        objfiles = []
        for o in args.objfiles:
            if not os.path.exists(o):
                print("Error: {} not found".format(o))
                sys.exit(1)

            if o.endswith(".a") or o.endswith(".rlib"):
                objfiles.append(ArchiveFile.from_file(o))
            else:
                objfiles.append(ObjFile.from_file(o))

        if args.diff:
            diff(objfiles)
        elif args.link:
            link(objfiles)
        else:
            details(objfiles)
