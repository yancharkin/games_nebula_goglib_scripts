#!/usr/bin/python3
# Copyright (c) 2015 Felix Krull <f_krull@gmx.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import atexit
from collections import namedtuple
from configparser import ConfigParser
import io
import os.path
import shutil
import struct
import sys
import traceback

Resolution = namedtuple("Resolution",
                        "width height width_offsets height_offsets")
Executable = namedtuple("Executable", "comment resolutions")

# There's four places we have to patch the resolution values:
#  - A function starting at 0x238022 that gets called for each resolution
#    listed by the OS/display driver and checks whether it's in the internal
#    list of known resolutions (which has a number of odd low resolutions, but
#    tops out at 1600x1200) and returns the index of the matching known
#    resolution or 0. Here, we replace the values for one of the known
#    resolutions with ours so the desired custom resolutions gets matched and
#    assigned an index.
#  - Three further functions at 0x2381A1, 0x244533 and 0x244712 which contain
#    large switch...case statements that take one of the resolution indices and
#    in some form return the associated width and height values. Here, we
#    override the resolution values for the known resolution we are replacing.

EXE_NAME = "Battle_Realms_F.exe"
EXE_BACKUP = "Battle_Realms_F.exe.resolution-patch-backup"
INI_NAME = "Battle_Realms.ini"
INI_BACKUP = "Battle_Realms.ini.resolution-patch-backup"
DEFAULT_REPLACE = 0x13
EXECUTABLES = {
    2998272: Executable("GOG.com", {
        0x07: Resolution(512, 384,
                         [0x2380AD, 0x23822C, 0x2445C4, 0x2447B6],
                         [0x2380B5, 0x238235, 0x2445CE, 0x2447BF]),
        0x0B: Resolution(800, 600,
                         [0x2380FA, 0x238273, 0x24460F, 0x2447FD],
                         [0x238102, 0x23827C, 0x244619, 0x244806]),
        0x0F: Resolution(1152, 864,
                         [0x23814B, 0x2382C3, 0x244663, 0x244844],
                         [0x238153, 0x2382CC, 0x24466D, 0x24484D]),
        0x13: Resolution(1600, 1200,
                         [0x23817B, 0x238313, 0x2446B7, 0x244894],
                         [0x238191, 0x23831C, 0x2446C1, 0x24489D]),
    }),
}


class UnknownExecutableError(Exception):
    pass


def pack_v(v):
    return struct.pack("<H", v)


def patch(f, res_desc, new_width, new_height):
    for offset in res_desc.width_offsets:
        f.seek(offset)
        f.write(pack_v(new_width))
    for offset in res_desc.height_offsets:
        f.seek(offset)
        f.write(pack_v(new_height))


def patch_ini(filename, new_width, new_height, encoding="latin1"):
    ini = ConfigParser(delimiters=("=",), empty_lines_in_values=False,
                       interpolation=None)
    ini.read(filename, encoding=encoding)
    ini["VideoState"]["Width"] = str(new_width)
    ini["VideoState"]["Height"] = str(new_height)
    # TODO: Are these changes necessary/helpful?
    ini["VideoState"]["Depth"] = "32"
    ini["VideoState"]["HardwareTL"] = "1"
    with open(filename, "w", encoding=encoding) as f:
        ini.write(f, space_around_delimiters=False)


def backup(filename, backup_name):
    if not os.path.exists(backup_name):
        shutil.copy(filename, backup_name)
    # Otherwise, we assume this is a backup from a previous run we shouldn't
    # override.


def patch_executable(filename, new_width, new_height, res_idx=DEFAULT_REPLACE):
    with open(filename, "r+b") as f:
        length = f.seek(0, io.SEEK_END)
        try:
            exe = EXECUTABLES[length]
        except KeyError:
            raise UnknownExecutableError(length)
        print("Found %s of %s bytes ('%s')..." %
              (EXE_NAME, length, exe.comment))
        res = exe.resolutions[res_idx]
        print("Replacing resolution 0x%X (default: %sx%s) with %sx%s..." %
              (res_idx, res.width, res.height, new_width, new_height))
        patch(f, res, new_width, new_height)


# Interface-y stuff.
def prompt_value(prompt, validate, invalid_msg):
    while True:
        try:
            inp = input(prompt)
            # Loop exit is here.
            return validate(inp)
        except ValueError:
            print(invalid_msg, inp)


def ask_new_res():
    def validate(s):
        v = int(s)
        if v <= 0 or v > 0xFFFF:
            raise ValueError
        return v
    error_msg = "Invalid value or not a number:"
    width = prompt_value("Enter new width: ", validate, error_msg)
    height = prompt_value("Enter new height: ", validate, error_msg)
    return (width, height)


def main():
    atexit.register(input, "Press Enter to exit...")

    try:
        print("""\
Battle Realms Resolution Patch

This patch allows Battle Realms to support custom higher resolutions,
including widescreen resolutions.
""")
        width, height = ask_new_res()
        backup(EXE_NAME, EXE_BACKUP)
        patch_executable(EXE_NAME, width, height)
        backup(INI_NAME, INI_BACKUP)
        patch_ini(INI_NAME, width, height)
        print("""\
Done. To switch to a different resolution, simply re-run this patch;
to remove it, restore the backup copies of %s and %s that were created
by this program. Enjoy!""" % (EXE_NAME, INI_NAME))
    except UnknownExecutableError as e:
        print("""\
Your version of %s (file size: %s bytes) is not supported by this patch.""" %
              (EXE_NAME, e.args[0]))
    except KeyboardInterrupt:
        print("Interrupted")
    except Exception:
        print("""\
An error occurred. The full error message is reproduced below; please
include it if you decide to ask for help with this issue.
""", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
