# win32-details extension for Nautilus

# Copyright 2022 tfuxu <tfuxu@tutanota.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import hashlib
import exiftool

import gi
gi.require_version('GdkPixbuf', '2.0')

from urllib.parse import unquote

from gi.repository import GObject, GLib, Gio, GdkPixbuf, Nautilus

'''details_list = [
    ["File Description", "EXE:FileDescription"],
    ["Comments", "EXE:Comments"],
    ["File Type", "File:FileType"],
    ["File Version", "EXE:FileVersionNumber"],
    ["Product Name", "EXE:ProductName"],
    ["Product Version", "EXE:ProductVersion"],
    ["Legal Copyright", "EXE:LegalCopyright"],
    ["File Size", "File:FileSize"],
    ["Modify Date", "File:FileModifyDate"],
    ["Language", "EXE:LanguageCode"]
]'''


class MorePropsModel(Nautilus.PropertiesModelProvider, GObject.GObject):
    def __init__(self):
        pass

    def log_debug(self, message):
        message = f"win32-details: {message}"
        variant_message = GLib.Variant("s", message)

        GLib.log_variant(None, GLib.LogLevelFlags.LEVEL_DEBUG, GLib.Variant("a{sv}", {"MESSAGE": variant_message}))

    def get_models(self, files):
        img_list = [
            ["Camera Brand", "EXIF:Make"],
            ["Camera Model", "EXIF:Model"],
            ["Exposure Time", "EXIF:ExposureTime"],
            #["Exposure Program", ""],
            ["Aperture Value", "EXIF:ApertureValue"],
            ["ISO Speed Rating", "EXIF:ISO"],
            ["Flash Fired", "EXIF:Flash"],
            ["Metering Mode", "EXIF:MeteringMode"],
            ["Exposure Mode", "EXIF:ExposureMode"],
            ["Focal Length", "EXIF:FocalLength"],
            ["Software", "EXIF:Software"],
            ["Title", "XMP:Title"],
            ["Description", "XMP:Description"],
            ["Keywords", "XMP:Subject"],
            ["Creator", "XMP:Creator"],
            ["Created On", "EXIF:DateTimeOriginal"],
            ["Copyright", "XMP:Rights"],
            ["Rating", "XMP:Rating"],
        ]

        # Reinitialize tags list
        tags = []

        # Reinitialize details list
        details_list = []

        # Check if its just a one file, or couple of files
        if len(files) != 1:
            self.log_debug("FILES INVASION!!!1")
            return

        # File path in its URI form
        file = files[0]

        # Convert URI to normal file path
        filename = unquote(file.get_uri()[7:])

        # Checkings, to ensure that we are dealing with a file and not with a shortcut or a folder
        if file.get_uri_scheme() != "file":
            return
        if file.is_directory():
            return

        # Create variables for basic image data
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(filename)
        pixinfo = pixbuf.get_file_info(filename)

        mime_type = file.get_mime_type()

        def is_mime_type_supported(mime_type):
            if mime_type == None:
                return False

            formats = pixbuf.get_formats()

            for format_list in formats:
                mime_types = format_list.get_mime_types()
                print(mime_types)

                if mime_types == None:
                    continue

                if mime_type in mime_types:
                    return True
            
            return False

        #file.is_mime_type(mime_type)

        self.log_debug(mime_type)

        # Check if file has a '.exe' extension
        print(f"is_mime_type_supported: {is_mime_type_supported}")
        if not is_mime_type_supported(mime_type):
            self.log_debug("Not valid")
            return


        # Retrieve image data and insert info to details_list
        def add_basic_info():
            name = pixinfo[0].get_name()
            desc = pixinfo[0].get_description()

            with exiftool.ExifToolHelper() as et:
                for orient_data in et.get_tags([filename], tags="EXIF:Orientation"):
                    print(f"orient_data: {orient_data.items()}")
                    meta, orient = orient_data.items() # FIXME: Some files doesn't include EXIF:Orientation tag
                    orientation = orient[1]
                    if (orientation == 6
                        or orientation == 8
                        or orientation == 7
                        or orientation == 4):
                        width = pixinfo[2]
                        height = pixinfo[1]
                    else:
                        width = pixinfo[1]
                        height = pixinfo[2]

            details_list.insert(0, ["Image Type", "{0} ({1})".format(name, desc)])
            details_list.insert(1, ["Width", "{0}px".format(width)])
            details_list.insert(2, ["Height", "{0}px".format(height)])

        # Get MD5 checksum of file and append info to details_list
        def add_md5sum_entry():
            md5sum = hashlib.md5(filename.encode("utf-8")).hexdigest()
    
            details_list.append(["MD5 Hash", md5sum])


        # The parsing machine
        with exiftool.ExifToolHelper(common_args=['-G', '-f']) as et:
            manifest = None
            for i in range(len(img_list)): # Move exiftool tags from imported img_list to local tags list
                tags.append(img_list[i][1])
            for entry in img_list: # Move list entries from img_list to details_list
                details_list.append(entry)
            for full_data in et.get_tags([filename], tags=tags):
                manifest = full_data
                manifest.pop("SourceFile")
            for i, (meta, data) in enumerate(manifest.items()):
                if meta == tags[i]:
                    if type(data) == str:
                        details_list[i][1] = data.strip()
                    else:
                        try:
                            details_list[i][1] = str(data)
                        except TypeError as e:
                            self.log_debug(f"Unexpected data type inside metadata. Exc: {e}")
                else:
                    details_list[i][1] = ""
                    continue
            add_basic_info()
            add_md5sum_entry()


        # Setup ListStore for Nautilus.PropertiesModel content model
        self.contentstore = Gio.ListStore.new(item_type=Nautilus.PropertiesItem)
        for details_ref in details_list:
            if details_ref[1] != "":
                list_item = Nautilus.PropertiesItem(
                    name = details_ref[0],
                    value = details_ref[1]
                )
                self.contentstore.append(list_item)


        # Return to API handler as Nautilus.PropertiesModel object
        return Nautilus.PropertiesModel(title="More Properties",
                                        model=self.contentstore),
