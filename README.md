# magic-lantern
A presentation tool for kiosks, digital signage, slide shows.

Supports *png* and *jpg*.  *PDF* files are also supported; each page is internally converted to an image file.

You can specify a single directory/folder for the images, or organise them into folders and provide a configuration file to control the sequence of images. This sequence is called the "*slide show*"



## Installation

### Windows
```PowerShell    
pip install magic-lantern
```

### Debian

```bash
pipx install magic-lantern
```

## Usage

See 

```bash
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

The format is TOML.  Comments are preceded by ***#***.

The first part of the file contains any default values.  They apply to all the subsequent albums if not overridden.  These are optional but are included in the example:

```toml
# Exclude the given list of dir names from the album image search.  
exclude=["_archive","archive","old","_old"]

# Default interval if not otherwise specifed.  This is the delay between images in the slide show
interval=3

# Default weighting applied to each album
weight=21
```

The remainder of the file organises the slide show by ***albums***.  Each album points to a directory containing images to include in the slide show.  Images are added automatically. Images can be separated into different albums depending on their intended behaviour in the display sequence.

```toml
[[albums]]
order="sequence" # These are picked in sequence
folder="images/numbers"
weight=1

[[albums]]
order="atomic" # These are "sticky"; they appear as a group, sequencially
folder="images/atomic"
weight=1

[[albums]]
order="random" # These appear randomly 
folder="images/paintings"
weight=1
```

When the slide show is generated, an image is taken from each album, randomly.  There is some control on this, based on provided weights.


# Notes

## Running over ssh
```bash
export DISPLAY=:0
```

## Fixing photo orientation 
[ImageMagick](https://imagemagick.org/script/mogrify.php)

```bash
mogrify -auto-orient *.jpg
```

## Fixing missing dates
e.g.: 

```bash
exiftool -datetimeoriginal="2009:08:08 00:00:00" -overwrite_original -m *
```

## What's with the name?
[Magic lantern](https://en.wikipedia.org/wiki/Magic_lantern)