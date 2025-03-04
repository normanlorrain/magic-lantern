# magic-lantern
A presentation tool for kiosks, digital signage, slide shows.

Supports *png* and *jpg*.  *PDF* files are also supported; each page is internally converted to an image file.

You can specify a single directory/folder for the images, or organise them into folders and provide a configuration file to control the sequence of images. This sequence is called the "*slide show*".



## Installation

### Windows

[pipx](https://pipx.pypa.io/stable/), via [Scoop](https://scoop.sh/)

```
scoop install pipx
pipx ensurepath
pipx install magic-lantern
```

### Debian

```bash
pipx install magic-lantern
```

## Usage

See 

```bash
magic-lantern --help
Usage: magic-lantern [OPTIONS] [DIRECTORY]

  A slide show generator. Specify a directory containing image files or use -c
  to specify a config file.

Options:
  --version                     Show the version and exit.
  -c, --config-file FILE        Configuration file.
  -f, --fullscreen              Full screen mode
  -s, --shuffle                 Shuffle the slides
  -d, --dry-run INTEGER RANGE   Test mode.  Only display the slide names.
                                Specify the number of slides.  [x>=1]
  -i, --interval INTEGER RANGE  Interval (seconds) between images.  [x>=1]
  -e, --exclude TEXT            Exclude the given directories.  Multiple
                                entries are permitted.
  --help                        Show this message and exit.
```

When running, use the following keys to control the slideshow:
- **space bar**: play / pause
- **q**: quit
- **p**, **left arrow**: previous image
- **n**, **right arrow**: previous image
- **y**, display of year (on/off)

## Reset

To reload the configuration and slide show: 
```bash
pkill -USR1 magic-lantern
```

This is useful if you have the app running automatically (e.g. Gnome autostart) and have updated the slide show.

## Configuration 
You can provide a simple path to a collection of images...

```
magic-lantern /usr/share/backgrounds
```

... or you can supply a configuration file:
```
magic-lantern -c ~/slideshow/example.toml
```
See [example.toml](docs/example.toml).  

The configuration file can specify multiple ***albums*** to include in the slideshow.  The behaviour of each album can be unique.  The file contains two sections:

- The first part of the file contains any default/global values.  They apply to all the subsequent albums if not overridden.  These are optional but are included in the example.

- The remainder of the file defines the albums.  Each album points to a directory containing images to include in the slide show.  Images are added automatically. Images can be separated into different albums depending on their intended behaviour. 
Options given here override the defaults provided previously.

### TOML configuration keys

This is a list of keys, their scope, etc., defined in the configuration file:

#### exclude
- *scope*: global 
- *type*: list of strings
- *value*: list the folders to exclude from the image search
- *default*: empty list.  All png/jpg/pdf files will be included.

#### fullscreen
- *scope*: global
- *type*: bool
- *value*: turn on full-screen mode
- *default*: false

#### weight
- *scope*: global and album
- *type*: integer
- *value*: give the weight to an album when choosing them randomly. When the slide show is generated, each image is taken from each album, chosen [randomly](https://docs.python.org/3/library/random.html#random.choices), according the the given weights.

- *default*: 1

#### interval
- *scope*: global and album
- *type*: integer
- *value*: give the time in seconds after a slide before the next one. 
- *default*: 5

#### shuffle
- *scope*: global
- *type*: bool
- *value*: randomize the output
  - for a single directory, all the photos are "shuffled"
  - for a configuration with multiple albums, the selection of albums is randomized. (The selection of photos within an album is governed in the album scope)
- *default*: false
  
#### [[albums]]
In TOML this specifies an array of key/value pairs.  Each of these entries define each album being configured. 

#### folder
- *scope*: album
- *type*: string
- *value*: points to the path of the directory containing the album.  Can be an absolute path, or relative to the configuration file.

#### order
- *scope*: album
- *type*: one of
    - `"sequence"`: photos in this album are picked in sequence
    - `"random"`: photos in this album are picked randomly
    - `"atomic"`: photos in this album are picked in sequence, and grouped together.  Once each image has been displayed, the slide show resumes with the next.
- *value*: defines the behaviour of the slideshow for each album.
- *default*: `"sequence"`


