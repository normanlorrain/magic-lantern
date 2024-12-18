# PDF pages to images for the slideshow.

import os
import pymupdf
import tempfile

from magic_lantern import log

_tempDir = None


def convert(pathName, fileName):
    global _tempDir
    if _tempDir is None:
        _tempDir = tempfile.TemporaryDirectory(
            suffix=None,
            prefix=None,
            dir=None,
            ignore_cleanup_errors=False,
        )
        log.debug(f"Temp Dir: {_tempDir.name}")
    doc = pymupdf.open(os.path.join(pathName, fileName))  # open document
    for page in doc:  # iterate through the pages
        pix = page.get_pixmap(dpi=600)  # render page to an image
        name = f"{fileName}-page-{page.number}.png"
        log.info(f"    {name}")
        pixFile = os.path.join(_tempDir.name, name)
        pix.save(pixFile)  # store image as a PNG
        yield pixFile
