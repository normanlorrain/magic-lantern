# magic-lantern
A presentation tool for kiosks, digital signage, slide shows.

Supports *png* and *jpg*.  *PDF* files are also supported; each page is internally converted to an image file.

You can specify a single directory/folder for the images, or organise them into folders and provide a configuration file to control the sequence of images. This sequence is called the "*slide show*".



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

The first part of the file contains any default/global values.  They apply to all the subsequent albums if not overridden.  These are optional but are included in the example:

```toml
# Exclude the given list of dir names from the album image search.  
exclude=["_archive","archive","old","_old"]

# Turn on full screen mode
fullscreen=true

# Default interval if not otherwise specifed.  This is the delay between images in the slide show
interval=3

# Default weighting applied to each album
weight=1
```

The remainder of the file organises the slide show by ***albums***.  Each album points to a directory containing images to include in the slide show.  Images are added automatically. Images can be separated into different albums depending on their intended behaviour.

Options given here override the defaults provided previously.

```toml
[[albums]]
folder="images/numbers"
order="sequence" # These are picked in sequence

[[albums]]
folder="images/atomic"
order="atomic" # These are "sticky"; they appear as a group, sequentially

[[albums]]
folder="images/paintings"
order="random" # These appear randomly 
weight=2
```

When the slide show is generated, each image is taken from each album, chosen [randomly](https://docs.python.org/3/library/random.html#random.choices), according the the given weights.


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