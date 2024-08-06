# magic-lantern
A presentation tool for kiosks, digital signage, slide shows.

Supports *png* and *jpg*.  *PDF* files are also supported; each page is internally exported to an image file.
## Installation

### Windows
```
pip install magic-lantern
```

### Debian

```
pipx install magic-lantern
```

## Usage

See 

```
magic-lantern --help
```

When running, use the following keys to control the slideshow:
- **space bar**: play / pause
- **q**: quit
- **p**, **left arrow**: previous image
- **n**, **right arrow**: previous image
- **y**, display of year (on/off)

## Configuration 
You can provide a simple path to a collection of images, or you can supply a configuration file.  See the example in `tests`.  


# Notes

## Fixing photo orientation 
[ImageMagick](https://imagemagick.org/script/mogrify.php)

```
mogrify -auto-orient *.jpg
```

## Fixing missing dates
e.g.: 

```
exiftool -datetimeoriginal="2009:08:08 00:00:00" -overwrite_original -m *
```

## Origin of the name
[Magic lantern](https://en.wikipedia.org/wiki/Magic_lantern)