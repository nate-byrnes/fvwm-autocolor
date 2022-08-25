#!/usr/bin/env python

import sys
import random
import os
import extcolors
from extcolors import command
from colour import Color

x_display = os.environ.get("DISPLAY", ":0.0")
home = os.environ.get('HOME', '.')
fvwmdir = os.environ.get('FVWM_USERDIR', home + os.path.sep + ".fvwm")
imgdir = os.environ.get('FAT_IMG_DIR', fvwmdir + os.path.sep + 'bg')
cachedir = os.environ.get('FAT_CACHE_DIR', imgdir)
swatchdir = os.environ.get('FAT_SWATCH_DIR', cachedir)
saveswatches = bool(int(os.environ.get('FAT_SAVE_SWATCH', '0')))
fvwmcommand = os.environ.get('FAT_FVWMCOMMAND', '/usr/bin/FvwmCommand')
bgcmd = os.environ.get('FAT_BG_COMMAND', '/usr/bin/feh --bg-tile --zoom 100 -D 3 -z')
inactive_colorsets = os.environ.get('FAT_INACT_COLORSETS', '0,1,3,5,7')
active_colorsets = os.environ.get('FAT_ACTIVE_COLORSETS', '2,4,6,8')


class LColor(Color):
   def __lt__(self, other):
      if self.get_luminance() < other.get_luminance():
         return True
      elif self.get_saturation() < other.get_saturation():
         return True
      elif self.get_hue() < other.get_hue():
         return True
      else:
         return False


def tuple_to_hex(t):
   r = hex(t[0])[2:]
   g = hex(t[1])[2:]
   b = hex(t[2])[2:]
   
   if len(r) == 1:
      r = "0" + r
   if len(g) == 1:
      g = "0" + g
   if len(b) == 1:
      b = "0" + b
   rv = f"#{r}{g}{b}"
   
   return rv


def fvwmcmd(string):
   os.system(f"{fvwmcommand} '{string}'")


def setbg(img):
   os.system(f"{bgcmd} {img}")


def extract_colorsets(img):
   imgfname = img.split(os.path.sep)[-1]
   cachefname = cachedir + os.path.sep + imgfname + ".colors"
   swatchfname = swatchdir + os.path.sep + imgfname + ".png"

   print(f"{imgfname} {cachefname} {swatchfname}")

   colors, px = extcolors.extract_from_path(img, limit=4)
   if saveswatches:
      command.image_result(colors, 256, swatchfname)
   if len(colors) == 1:
      c1 = tuple_to_hex(colors[0][0])
      C1 = LColor(c1)
      C1.set_luminance(C1.get_luminance() * 0.8)
      c2 = C1.get_web()
      C1.set_luminance(C1.get_luminance() * 0.8)         
      c3 = c1
      c4 = C1.get_web()
   elif len(colors) == 2:
      c1 = tuple_to_hex(colors[0][0])
      c2 = tuple_to_hex(colors[1][0])

      C1 = LColor(c1)
      C1.set_luminance(C1.get_luminance() * 0.5)
      c3 = C1.get_web()

      c3 = c2

      C2 = LColor(c2)
      C2.set_luminance(C2.get_luminance() * 0.5)
      c4 = C2.get_web()
   elif len(colors) == 3:
      c1 = tuple_to_hex(colors[0][0])
      c2 = tuple_to_hex(colors[1][0])
      c3 = tuple_to_hex(colors[1][0])
      c4 = tuple_to_hex(colors[2][0])
   else:
      c1 = tuple_to_hex(colors[0][0])
      c2 = tuple_to_hex(colors[1][0])
      c3 = tuple_to_hex(colors[2][0])
      c4 = tuple_to_hex(colors[3][0])

      # sort for a lighter foreground pair
      C1 = LColor(c1)
      C2 = LColor(c2)
      C3 = LColor(c3)
      C4 = LColor(c4)
      
      C3, C4, C1, C2 = sorted([C1, C2, C3, C4])
      
      c1, c2, c3, c4 = C1.get_web(), C2.get_web(), C3.get_web(), C4.get_web()

   with open(cachefname, 'w') as f:
      f.write(f"{c1},{c2},{c3},{c4}")
   
   return c1, c2, c3, c4


def send_colorsets(img):
   imgfname = img.split(os.path.sep)[-1]
   cachefname = cachedir + os.path.sep + imgfname + ".colors"

   print(f"- {img} - {imgfname} - {cachefname} - ")

   try:
      with open(cachefname, 'r') as f:
         c1, c2, c3, c4 = f.read().strip().split(',')
   except FileNotFoundError:
      c1, c2, c3, c4 = extract_colorsets(img)

   # sort for a lighter foreground pair
   C1 = LColor(c1)
   C2 = LColor(c2)
   C3 = LColor(c3)
   C4 = LColor(c4)
   
   C1, C2, C3, C4 = sorted([C1, C2, C3, C4])
   
   # Map the ordered by luminance colors (darkest to lightest) as follows:
   # c2 -> inactive BG
   # c4 -> active BG
   # c1 -> inactive FG
   # c3 -> active FG
   c2, c4, c1, c3 = C1.get_web(), C2.get_web(), C3.get_web(), C4.get_web()

   # output the colors to stdout
   print(f"inactive fg: {c1} / bg: {c2}, active fg: {c3} / bg: {c4}")

   for cs in inactive_colorsets.split(','):
      fvwmcmd(f"ColorSet {cs} fg {c1}, bg {c2}, sh, hi, Plain, NoShape")

   for cs in active_colorsets.split(','):
      fvwmcmd(f"ColorSet {cs} fg {c3}, bg {c4}, sh, hi, Plain, NoShape")

   setbg(img)
   # fvwmcmd(f"DestroyMenu NewBGFromRand\nAddToMenu NewBGFromRand ImageFile Title\n+ {img} Nop\nPopup NewBGFromRand")
   # os.system("/usr/bin/feh " + imgdir + '/swatches/' + img.split('/')[-1] + '.png')


def sel_rand_img():
   files = os.listdir(imgdir)
   files = [x for x in files if not x.endswith('.colors')]
   img = files[int(random.random() * len(files))]
   send_colorsets(imgdir + os.path.sep + img)

if __name__ == '__main__':
   # Set the display so this can run in a cronjob if desired...
   os.environ["DISPLAY"] = x_display
   if sys.argv[1:]:
      send_colorsets(sys.argv[1])
   else:
      sel_rand_img()

