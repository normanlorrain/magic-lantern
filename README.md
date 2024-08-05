# magic-lantern
A presentation tool for kiosks, digital signage, slide shows.

Supports *png* and *jpg*.  *PDF* files are also supported; each page is internally exported to an image file.
## Installation

### Windows
`pip install magic-lantern`

### Debian

```
pipx install magic-lantern
```

## Usage

See 

`magic-lantern --help` . 

When running, use the following keys to control the slideshow:
- **space bar**: play / pause
- **q**: quit
- **p**, **left arrow**: previous image
- **n**, **right arrow**: previous image
- **y**, display of year (on/off)

## Configuration 
You can provide a simple path to a collection of images, or you can supply a configuration file.  See the example in `tests`.  


# Fixing images

Some notes on tweaking images if necessary.


## ImageMagick

### Fix photo orientation

mogrify -auto-orient *.jpg

### Fix missing dates
e.g.: 
exiftool -datetimeoriginal="2009:08:08 00:00:00" -overwrite_original -m *