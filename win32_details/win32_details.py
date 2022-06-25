# win32-details extension for Nautilus

# Copyright 2022 tfuxu <tfuxu@tutanota.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from urllib.parse import unquote
import hashlib

import exiftool
from gi.repository import Nautilus, Gtk, GObject


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


class DetailsPropPage(Nautilus.PropertyPageProvider, GObject.GObject):
    def __init__(self):
        pass

    def get_property_pages(self, files):
        # Check if its just a one file, or couple of files
        if len(files) != 1:
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
            #print(f"Range of manifest: {range(len(manifest)-1)}")
            #print(f"Range of tags: {range(len(tags))}")
            for meta, data in manifest.items():
                for i, mtags in zip(range(len(tags)), tags):
                    #print(meta == mtags)
                    if meta == mtags:
                        details_list[i][1] = data.strip()
                    else:
                        continue
            details_list[-1][1] = md5sum


        # Setup title for page
        self.page_title = Gtk.Label("Details")
        self.page_title.show()

        # Setup main vertical box
        self.vbox = Gtk.VBox(homogeneous=False)
        self.vbox.show()

        # Setup ListStore for TreeView
        self.tree_liststore = Gtk.ListStore(str, str)
        for details_ref in details_list:
            self.tree_liststore.append(list(details_ref))

        # Setup details TreeView
        self.treeview = Gtk.TreeView(model=self.tree_liststore)
        self.treeview.set_hover_selection(True)
        for i, column_title in enumerate(["Property", "Value"]):
            renderer = Gtk.CellRendererText()
            if column_title == "Value":
                renderer.set_property("editable", True)
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)
        self.treeview.show()
        self.vbox.pack_start(self.treeview, False, False, 0)


        # Return to API handler as Nautilus.PropertyPage object
        return Nautilus.PropertyPage(name="win32-details-page",
                                     label=self.page_title, 
                                     page=self.vbox),
