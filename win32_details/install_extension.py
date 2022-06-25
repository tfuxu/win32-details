# win32-details extension for Nautilus

# Copyright 2022 tfuxu <tfuxu@tutanota.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import os, sys
import shutil
import argparse

from . import VERSION


XDG_DATA_DIR = os.environ.get("XDG_DATA_DIR", "/usr/share")
XDG_DATA_HOME = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))

dest_system = os.path.join(XDG_DATA_DIR, "nautilus-python/extensions")
dest_user = os.path.join(XDG_DATA_HOME, "nautilus-python/extensions")

root_dir = os.path.abspath(os.path.dirname(__file__))


""" Installation functions section """
def install_system():
    if not os.path.isdir(dest_system):
        os.makedirs(dest_system)
    shutil.copy(os.path.join(root_dir, "win32_details.py"), os.path.join(dest_system, "win32_details.py"))

def uninstall_system():
    os.remove(os.path.join(dest_system, "win32_details.py"))

def install_user():
    if not os.path.isdir(dest_user):
        os.makedirs(dest_user)
    shutil.copy(os.path.join(root_dir, "win32_details.py"), os.path.join(dest_user, "win32_details.py"))

def uninstall_user():
    os.remove(os.path.join(dest_user, "win32_details.py"))


""" Argparse action classes section """
class InstallSystemExtension(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if os.getuid() != 0:
            print("\33[31m[ERROR]\33[0m: You need to run this command as root to perform a system-wide installation.")
            sys.exit(1)
        install_system()
        sys.exit(0)

class UninstallSystemExtension(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if os.getuid() != 0:
            print("\33[31m[ERROR]\33[0m: You need to run this command as root to perform a system-wide removal.")
            sys.exit(1)
        uninstall_system()
        sys.exit(0)

class InstallUserExtension(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if os.getuid() == 0:
            print("\33[31m[ERROR]\33[0m: You need to run this command as regular user to perform a local installation.")
            sys.exit(1)
        install_user()
        sys.exit(0)

class UninstallUserExtension(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if os.getuid() == 0:
            print("\33[31m[ERROR]\33[0m: You need to run this command as regular user to perform a local removal.")
            sys.exit(1)
        uninstall_user()
        sys.exit(0)


""" CLI parser section (parser init and arguments) """
def cli_main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(prog="win32-details")

    parser.add_argument("-V", "--version",
                        help="print version and exit",
                        action="version",
                        version=VERSION)

    parser.add_argument("--install-system",
                        help="Install Win32 Details extension system-wide and exit",
                        nargs=0,
                        action=InstallSystemExtension)

    parser.add_argument("--uninstall-system",
                        help="Uninstall Win32 Details extension system-wide and exit",
                        nargs=0,
                        action=UninstallSystemExtension)

    parser.add_argument("--install-user",
                        help="Install Win32 Details extension for the current user and exit",
                        nargs=0,
                        action=InstallUserExtension)

    parser.add_argument("--uninstall-user",
                        help="Uninstall Win32 Details extension for the current user and exit",
                        nargs=0,
                        action=UninstallUserExtension)

    if len(args) == 0:
        parser.parse_args(["--help"])
    else:
        parser.parse_args(args)


if __name__ == "__main__":
    cli_main()
