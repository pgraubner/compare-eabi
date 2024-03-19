#!/usr/bin/python3

import subprocess
import io

from arm_eabi_diagnostics import Diagnostics
from arm_tags import *

EMPTY = '<EMPTY>'

class bcolors:
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

def all_equal_or_empty(elements):
   first = EMPTY
   for item in elements:
      if item == EMPTY:
         continue
      if item != first:
         if first != EMPTY:
            return False
         first = item

   return True

def all_empty(elements):
    return all(x == EMPTY for x in elements)

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
            objs.append(o.restrictions())
            #objs += o.objfiles()
         else:
            objs.append(o)

      attrs = {}
      for tag in Tags.keys():
         attrs[tag] = {}
         for obj in objs:
            val = EMPTY
            if tag in obj.attrs():
               val = obj.attrs()[tag]
            attrs[tag][obj.filename()] = val

      result = Diff(attrs)
      return result

   def __repr__(self) -> str:
      return repr(self.__objfiles)


class Diff:
   DIFF_PROPERTIES = {'identical': {'header': 'Identical tags\n', 'color': bcolors.OKGREEN},
               'identical-or-empty': {'header': 'Identical tags with empty values\n', 'color': bcolors.OKGREEN},
               'non-identical': {'header': 'Tags with non-identical (possibly conflicting) values\n', 'color': bcolors.FAIL}
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
            if all_empty(val.values()):
               continue
            self.__properties['identical'].append(attr)
         elif all_equal_or_empty(val.values()):
            self.__properties['identical-or-empty'].append(attr)
         else:
            self.__properties['non-identical'].append(attr)

   def property(self, prop):
      return self.__properties[prop]

   def __repr__(self) -> str:
      result = io.StringIO()

      def write_attr(attr, val):
         if verbose:
            result.write(attr)
            result.write(":")
            result.write(repr(val))
            result.write(Diagnostics[attr])
         else:
            result.write(attr)
            result.write(":")
            result.write(repr(val))

      def write_property(key):
         property = Diff.DIFF_PROPERTIES[key]
         result.write(bcolors.HEADER)
         result.write(property['header'])
         result.write(bcolors.ENDC)

         for attr in self.property(key):
            result.write(property['color'])
            write_attr(attr, self.__attrs[attr])
            result.write(bcolors.ENDC)
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

   def restrictions(self):
      attrs = {}
      for tag in Tags.keys():
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
      global readelf
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

   @staticmethod
   def from_file(filename):
      out = subprocess.run([readelf, "-A", filename], stdout=subprocess.PIPE)
      buf = io.StringIO(out.stdout.decode('utf-8'))
      return ObjFile.from_buf(filename, buf)

   @staticmethod
   def from_buf(filename, buf):
      global readelf

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
            attrs[key.strip()] = value.strip()

      result = ObjFile(filename, attrs)
      return result

   def __repr__(self) -> str:
      result = io.StringIO()
      result.write(bcolors.BOLD)
      result.write(self.filename())
      result.write(bcolors.ENDC)
      result.write("\n")

      for attr, val in self.__attrs.items():
         num = None
         info = get_tag_info(attr)
         if info is not None:
            num = info.index(val)
         if verbose:
            result.write(bcolors.HEADER)
            result.write(attr)
            result.write(": ")
            result.write(val)
            if num is not None:
               result.write(" ({})".format(num))
            result.write(bcolors.ENDC)
            result.write(Diagnostics[attr])
         else:
            result.write(attr)
            result.write(": ")
            result.write(val)
            if num is not None:
               result.write(" ({})".format(num))
         result.write("\n")

      return result.getvalue()

   def compare(self, other):
      assert self._section_name == other._section_name

      delta =  {}
      for attr in self.__attrs.keys():
            a = self.__attrs[attr]
            if attr in other._attrs:
               b = other._attrs[attr]
               if a != b:
                  delta[attr] = ((self.__fn, a), (other._fn, b))
            else:
               delta[attr] = (self.__fn, a)

      for attr in other._attrs.keys():
            if attr in delta:
               continue
            if attr not in self.__attrs:
               b = other._attrs[attr]
               if a != b:
                  delta[attr] = (other._fn, b)
      return delta

   def filename(self):
      return self.__fn

def diff(objfiles):
    objs = ObjFilelist.from_array(objfiles)
    print(objs.compare())

def details(objfiles):
   global verbose
   for o in objfiles:
      print(o)

def link(objfiles):
   global ld
   global ldflags
   global ldstaticlibs

   import tempfile
   with tempfile.TemporaryDirectory() as tmpdirname:
      files = [obj.filename() for obj in objfiles]
      elffile = "{}/test.elf".format(tmpdirname)
      flags = ldflags.split(" ") if ldflags != "" else []
      staticlibs = ldstaticlibs.split(" ") if ldstaticlibs != "" else []
      out = subprocess.run([ld, "-o", elffile, *flags, *files, *staticlibs])
      if out.returncode == 0:
         details([ObjFile.from_file(elffile)])

readelf = "readelf"
verbose = False
ld = "ld"
ldflags = ""
ldstaticlibs = ""

if __name__ == '__main__':
   import shutil
   import sys
   import os
   import argparse

   parser = argparse.ArgumentParser(
                  prog='eabi-helper',
                  description='helps interpreting objects file in ARM32 ABI')
   parser.add_argument('--objfiles', nargs='+')
   parser.add_argument('--verbose', action='store_true')
   parser.add_argument('--diff', action='store_true')
   parser.add_argument('--link', action='store_true')
   parser.add_argument('--readelf', nargs=1)
   parser.add_argument('--ld', nargs=1)
   parser.add_argument('--ldflags', nargs=1)
   parser.add_argument('--ldstaticlibs', nargs=1)
   parser.add_argument('--explain', action='store', type=str)

   args = parser.parse_args()

   if args.explain is not None:
      if args.explain not in Tags:
         print("Error: {} not a valid tag".format(args.explain))
         sys.exit(1)
      if args.explain not in Diagnostics:
         print("Error: {} has no diagnostics information".format(args.explain))
         sys.exit(1)
      print(bcolors.BOLD, args.explain, bcolors.ENDC)
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
