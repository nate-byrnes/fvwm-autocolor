# fvwm-autocolor
Simple script to change colors automatically in an attempt to match an image, which it will call a command to set as the desktop background

# Installation
```sh
git clone https://github.com/nate-byrnes/fvwm-autocolor.git
cd fvwm-autocolor
cp autotheme.py ${HOME}/.fvwm/
pip install -r requirements.txt
```

# FVWM Integration

The script operates on the the following environment variables:
1. DISPLAY
1. FVWM_USERDIR (set by FVWM, but cron won't see it ...)
1. FAT_IMG_DIR (defaults to ${FVWM_USERDIR}/bg}, where random mode will pick images from)
1. FAT_CACHE_DIR (defaults to ${FAT_IMG_DIR}, where extracted colors are cached, mapped to filename.colors)
1. FAT_SWATCH_DIR (defaults to ${FAT_CACHE_DIR}, where extracted swatches can be stored, also, mapped to filename)
1. FAT_SAVE_SWATCH (Defaults to 0 for disabled, 1 to enable the saving of extraced swatches)
1. FAT_FVWMCOMMAND (defaults to /usr/bin/FvwmCommand, used to tell FVWM the changes to the colorsets)
1. FAT_BG_COMMAND (defaults to '/usr/bin/feh --bg-tile --zoom 100 -D 3 -z' to set the desktop background)
1. FAT_INACT_COLORSETS (default '0,1,3,5,7' the numbers of the inactive colorsets to modify)
1. FAT_ACTIVE_COLORSETS (default '2,4,6,8' the numbers of the active colorsets to modify)

Configuration notes:
Need to have ```FvwmCommandS``` module running so that FvwmCommand can communicate with the window manager.

Here is a simple function that can be added to menu items or decoration buttons or wherever to trigger a
new "auto theme" based upon a randomly selected image:

```
# Random Background Function
DestroyFunc FuncRandTheme
AddToFunc   FuncRandTheme
+ I Exec exec python $[FVWM_USERDIR]/autotheme.py
```

And, to start with a specific theme add the following to the start:
```
# Use a specific image file (in this case square-tiles.jpg) to autotheme from
AddToFunc   StartFunction
+ I Module FvwmCommandS
+ I Test (x $[FVWM_USERDIR]/autotheme.py) Exec exec $[FVWM_USERDIR]/autotheme.py $[FVWM_USERDIR]/bg/square-tiles.jpg
```

# Screenshots

![Tile](/main/screenshots/tiles.png?raw=true "Tiles")

![grey](/main/screenshots/grey.png?raw=true "Grey")

![Blossom Tree](/main/screenshots/fog_bloom.png?raw=true "Tree")

![Green](/main/screenshots/green2.png?raw=true "Green")

