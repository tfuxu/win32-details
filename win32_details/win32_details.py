# win32-details extension for Nautilus

# Copyright 2022 tfuxu <tfuxu@tutanota.com>
# SPDX-License-Identifier: GPL-3.0-or-later


import hashlib
import exiftool

from urllib.parse import unquote

from gi.repository import GObject, Gio, Nautilus, GLib


details_list = [
    ["File Description", ""],
    ["Comments", ""],
    ["File Type", ""],
    ["File Version", ""],
    ["Product Name", ""],
    ["Product Version", ""],
    ["Legal Copyright", ""],
    ["File Size", ""],
    ["Modify Date", ""],
    ["Language", ""],
    ["MD5 Hash", ""]
]

tags = [
    "EXE:FileDescription",
    "EXE:Comments",
    "File:FileType",
    "EXE:FileVersionNumber",
    "EXE:ProductName",
    "EXE:ProductVersion",
    "EXE:LegalCopyright",
    "File:FileSize",
    "File:FileModifyDate",
    "EXE:LanguageCode"
]


class MorePropsModel(Nautilus.PropertiesModelProvider, GObject.GObject):
    def __init__(self):
        pass

    def log_warn(self, message):
        GLib.log_variant(None, GLib.LogLevelFlags.LEVEL_DEBUG, GLib.Variant("a{sv}", {"MESSAGE": message}))

    def get_models(self, files):
        # Check if its just a one file, or couple of files
        if len(files) != 1:
            self.log_warn(GLib.Variant("s", "FILES INVASION!!!1"))
            return

        # File path in its URI form
        file = files[0]

        # Checkings, to ensure that we are dealing with a file and not with a shortcut or a folder
        if file.get_uri_scheme() != "file":
            return
        if file.is_directory():
            return

        # Check if file has a '.exe' extension
        if file.get_uri()[-4:] != ".exe":
            return


        # Clean details list before doing anything with it
        for i, value in enumerate(details_list):
            details_list[i][1] = ""

        # Convert URI to normal file path
        filename = unquote(file.get_uri()[7:])

        md5sum = hashlib.md5(filename.encode("utf-8")).hexdigest()


        # The parsing machine
        with exiftool.ExifToolHelper(common_args=['-G']) as et:
            manifest = None
            for full_data in et.get_tags([filename], tags=tags):
                manifest = full_data
                manifest.pop("SourceFile")
            for meta, data in manifest.items():
                for i, mtags in zip(range(len(tags)), tags):
                    if meta == mtags:
                        details_list[i][1] = data.strip()
                    else:
                        continue
            details_list[-1][1] = md5sum


        # Setup ListStore for Nautilus.PropertiesModel content model
        self.contentstore = Gio.ListStore.new(item_type=Nautilus.PropertiesItem)
        for details_ref in details_list:
            list_item = Nautilus.PropertiesItem(
                name = details_ref[0],
                value = details_ref[1]
            )
            self.contentstore.append(list_item)


        # Return to API handler as Nautilus.PropertiesModel object
        return Nautilus.PropertiesModel(title="More Properties",
                                        model=self.contentstore),
