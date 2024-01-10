import os
import logging as log


photoList = []


def init(src: str):
    for root, dirs, files in os.walk(src):
        log.info(f"In {root}")
        for f in files:
            if not f.lower().endswith((".png", ".jpg", ".jpeg")):
                log.warning(f"{f}  Unknown file type")
                continue
            photoList.append(os.path.join(src,f))

            # try:
            #     y, m, d = getDateFromFile(root, f)
            # except ValueError as e:
            #     log.warning(f"{f}, {e}, (File not processed)")
            #     continue
