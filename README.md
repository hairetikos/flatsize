![flatsize app window](https://github.com/hairetikos/flatsize/blob/main/flatsize.png)

# flatsize
change the various DPI scaling of flatpak apps using overrides.

since i wanted to check out codium, i noticed it didn't inherit the DPI scaling of my system, i had to set a GTK scaling override.

i wanted to use codium for AI-assisted coding, so i figured i would make a GUI program using AI to easily change the DPI, and included various types of DPI/scaling overrides.

# dependencies
  `python`
  `qt5`

debian:
  `apt install python3 python3-qtpy-pyqt5`

# small hurdles that had to be solved with copilot:

created via prompting copilot AI claude 3.7 thinking

it assumed `--csv` was available in flatpak, but my version is older
> you have flatpak but no --csv option

it was expecting regular spaces between columns, but the data was using tabs
> the output of flatpak list is using tab spaces, not normal spaces

it was expecting the first output line to have the headers
> within the python request, it does not include a header, so do not strip the first line
