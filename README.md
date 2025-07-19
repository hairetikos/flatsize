![flatsize app window](https://github.com/hairetikos/flatsize/blob/main/flatsize.png)

# flatsize
change the various DPI scaling of flatpak apps using overrides.

since i wanted to check out codium, i noticed it didn't inherit the DPI scaling of my system, i had to set a GTK scaling override.

i wanted to use codium for AI-assisted coding, so i figured i would make a GUI program using AI to easily change the DPI, and included various types of DPI/scaling overrides.

# dependencies
  `python3`
  `qt5`

Debian/Ubuntu/Mint

`# apt install python3 python3-qtpy-pyqt5`

Fedora/RHEL/CentOS

`# dnf install python3 python3-qt5`

Arch Linux/Manjaro

`# pacman -S python python-pyqt5`

openSUSE

`# zypper install python3 python3-qt5`

Other Distributions

Install Python 3 and PyQt5 using your distribution's package manager, then if needed:

`$ pip install PyQt5`

# usage
  `$ python3 flatsize.py`
  
  or
  
  `$ chmod +x flatsize.py`
  
  `$ ./flatsize.py`
  
  copy to system binary location for easy invocations
  
  usually just one simple override needs to be set (such as GTK for GTK apps, QT for QT apps, etc)
  
# small hurdles that had to be solved to help copilot:

created via prompting copilot AI claude 3.7 thinking

it assumed `--csv` was available in flatpak, but my version is older
> you have flatpak but no --csv option

it was expecting regular spaces between columns, but the data was using tabs
> the output of flatpak list is using tab spaces, not normal spaces

it was expecting the first output line to have the headers
> within the python request, it does not include a header, so do not strip the first line
