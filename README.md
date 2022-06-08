# Win32 Details
![License](https://img.shields.io/github/license/tfuxc/win32-details)

> .exe file details for your Nautilus file browser

**Win32 Details** is an additional page in Properties dialog named `Details`, similar to that from Windows File Explorer. It allows to conveniently display a specific details about .exe files within comfort of your file browser.

## How to use it
Just right-click on any .exe file, go to Properties, and click `Details` tab.

## Installation
### Requirements
* Probably could be even a **Nautilus 2.32.x**, but I'm not sure, you can test that if you want :)
* Copy of [exiftool](https://github.com/exiftool/exiftool) installed globally on system
* [nautilus-python](https://wiki.gnome.org/Projects/NautilusPython)

### From source
**[NOTE]** This is the only option, because I didn't submitted this extension to PyPI or AUR yet, so there isn't any 'easy' approach for now.

**1.** Clone the repository, and cd to it:
```
git clone https://github.com/tfuxc/win32-details.git
cd win32-details
```

**2.** Install Python requirements:
```
pip install -r requirements.txt
```

**3.** Now you need to copy `win32-details.py` file to one of those locations:

`~/.local/share/nautilus-python/extensions/` - User install:
```
cp win32-details.py ~/.local/share/nautilus-python/extensions/win32-details.py
```

`/usr/share/nautilus-python/extensions/` - System-wide install:
```
sudo cp win32-details.py /usr/share/nautilus-python/extensions/win32-details.py
```

**4.** Close current Nautilus instances to load extension:
```
nautilus -q
```

## Screenshots
