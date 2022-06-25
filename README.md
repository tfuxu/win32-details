# Win32 Details
![License](https://img.shields.io/github/license/tfuxu/win32-details)

**Win32 Details** is an additional page in Properties dialog named `Details`, similar to that from Windows File Explorer. It allows to conveniently display a specific details about .exe files within comfort of your file browser.

![win32-details v0.1](https://raw.githubusercontent.com/tfuxu/win32-details/main/data/images/win32-details-screenshot-1.png)

## How to use it
Just right-click any .exe file, go to Properties, and click `Details` tab.

## Installation
### Requirements
* **Python** >= 3.6,
* Probably a recent version of **Nautilus 3.x**, or **Nautilus 4x**,
* [nautilus-python](https://wiki.gnome.org/Projects/NautilusPython),
* Copy of [exiftool](https://github.com/exiftool/exiftool) (required by PyExifTool),
* [PyExifTool](https://pypi.org/project/PyExifTool/)

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

### From source
Clone the repository, and cd to it:
```
git clone https://github.com/tfuxu/win32-details.git
cd win32-details
```

Win32 Details can be installed system-widely or just for the current user.

User install:
```
pip3 install --user .
win32-details --install-user
```

System-wide install:
```
sudo pip3 install .
sudo win32-details --install-system
```

Close currently opened Nautilus instances to load the extension:
```
nautilus -q
```

## Changelog
* **0.4:**
    * Add a `MD5 Hash` row
    * Allow user to copy values from rows (if row is selected, click left one time to select text)
    * Add setup.py for packaging to PyPI
    * Create a small CLI tool for easier installing (based on [Nautilus Terminal](https://github.com/flozz/nautilus-terminal/blob/master/nautilus_terminal/__main__.py))
* **0.1:**
    * Initial release of Win32 Details