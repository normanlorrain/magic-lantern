# magic-lantern
A presentation tool for kiosks, digital signage, slide shows.

Supports *png* and *jpg*.  *PDF* files are also supported; each page is internally exported to an image file.
## Installation

`pip install magic-lantern`

## Usage

See 

`magic-lantern --help` . 

## Configuration 
You can provide a simple path to a collection of images, or you can supply a configuration file.  See the example in `tests`.  

## Linux requirements
- click
- pygame
  - libsdl2-dev
  - python3-dev


### Pygame  
I had to install pygame to get the full image features.  

To test if necessary, to this 

    python -c "import pygame;print(pygame.image.get_extended())"

If you get a failure, install per [instructions](https://www.pygame.org/wiki/CompileUbuntu?parent=#Python%203.x): 

    #install dependencies
    sudo apt-get install git python3-dev python3-setuptools python3-numpy python3-opengl \
        libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev \
        libsdl1.2-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev \
        libtiff5-dev libx11-6 libx11-dev fluid-soundfont-gm timgm6mb-soundfont \
        xfonts-base xfonts-100dpi xfonts-75dpi xfonts-cyrillic fontconfig fonts-freefont-ttf libfreetype6-dev

    # Grab source
    git clone git@github.com:pygame/pygame.git

    # Finally build and install
    cd pygame
    python3 setup.py build
    sudo python3 setup.py install


I also needed to install -U cython for the above to work. Your mileage may vary, depending on the state of the installed versions of these libraries.


# Fixing images

Some notes on tweaking images if necessary.


## ImageMagick

### Fix photo orientation

mogrify -auto-orient *.jpg

### Fix missing dates
e.g.: 
exiftool -datetimeoriginal="2009:08:08 00:00:00" -overwrite_original -m *