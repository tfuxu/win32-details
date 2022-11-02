# Win32 Details
![PyPI](https://img.shields.io/pypi/v/win32-details)
![License](https://img.shields.io/github/license/tfuxu/win32-details)

**Win32 Details** is an additional page in Properties dialog named `Details`, similar to that from Windows File Explorer. It allows to conveniently display a specific details about .exe files within a comfort of your file browser.

![win32-details v0.1](https://raw.githubusercontent.com/tfuxu/win32-details/main/data/images/win32-details-screenshot-1.png)

## How to use it
Just right-click any .exe file, go to Properties, and click `Details` tab.

## Installation
### From PyPI
Win32 Details can be installed system-widely or just for the current user.

User install:
```
pip3 install --user win32-details
win32-details --install-user
```

System-wide install:
```
sudo pip3 install win32-details
sudo win32-details --install-system
```

Close currently opened Nautilus instances to load the extension:
```
nautilus -q
```

## Building from source
### Prerequisites
The following packages are required to build win32-details:

* **Python** >= 3.6,
* A recent version of **Nautilus >= 43.x**,
* [nautilus-python](https://wiki.gnome.org/Projects/NautilusPython),
* Copy of [exiftool](https://github.com/exiftool/exiftool) (required by PyExifTool),
* [PyExifTool](https://pypi.org/project/PyExifTool/)
* Meson and Ninja build systems (only needed for [Using Meson](#using-meson) build option)

Required Python libraries:
```
pip install -r requirements.txt
```

### Build instructions
Clone the repository:
```
git clone https://github.com/tfuxu/win32-details.git
cd win32-details
```

#### As a library:
Local installation:
```
pip3 install --user .
win32-details --install-user
```

System-wide installation:
```
sudo pip3 install .
sudo win32-details --install-system
```

#### Using Meson:
Local installation:
```
meson builddir --prefix="$HOME/.local"
ninja -C builddir install
```

System-wide installation:
```
meson builddir --prefix=/usr
sudo ninja -C builddir install
```

> **Warning**
> If you get a `Directory already configured` message when running `meson builddir` command, you can append to this command `--wipe` option to clean build directory before configuration.

Close currently opened Nautilus instances to load the extension:
```
nautilus -q
```

## Note about Nautilus versions below 43.x
Support for older Nautilus versions has been removed in win32-details 0.5.0, because of moving to Nautilus API 4.0, which deprecates direct usage of GTK widgets in favor of a new model-based interface (which is a shitty decision IMO). In this situation I had three options:
- Maintain both versions of extension, one for Nautilus 43 and above, and one for Nautilus <= 42,
- Make this extension as a standalone program, and use extension to launch it,
- Just deprecate support for older Nautilus versions.

Honestly, I'm not that interested in maintaining a seperate version of extension, as majority of people are using the latest version of Nautilus now. Moving a extension to a standalone program would make everything more complicated, and I don't think that many people would want to install an app which just shows them details of EXE files (but maybe, in the [future](https://github.com/tfuxu/win32-details/issues/5)...).

## License
<p>
<img src="https://www.gnu.org/graphics/gplv3-with-text-136x68.png" alt="GPLv3 logo" align="right">
This repository is licensed under the terms of the GNU GPLv3 license. You can find a copy of the license in the LICENSE file.
</p>

## Changelog
* **0.5.0:**
    * Port extension to Nautilus API 4.0, **from this version onward, win32-details won't support Nautilus versions below 43**[ (more info)](#note-about-nautilus-versions-below-43x)
    * Add new Meson build option
    * Change page name to `More Properties`
* **0.4.0:**
    * Add a `MD5 Hash` row
    * Allow user to copy values from rows (if row is selected, click left one time to select text)
    * Add setup.py for packaging to PyPI
    * Create a small CLI tool for easier installing (based on [Nautilus Terminal](https://github.com/flozz/nautilus-terminal/blob/master/nautilus_terminal/__main__.py))
* **0.1.0:**
    * Initial release of Win32 Details