"""ImageUtils"""

import io
from PIL import Image, ExifTags

def fix_image_orientation(image_file):
    """
    Takes a file name or file-like object.
    Returns the image with the image rotated to correct for orientation.
    """

    img = Image.open(image_file)
    original_format = img.format
    exif = img.getexif()

    # Obtain EXIF encoded orientation
    orientation = None
    for o in ExifTags.TAGS.keys():
        if ExifTags.TAGS[o]=='Orientation':
            orientation = o
            break

    # Rotate image and reset the orientation
    if orientation and orientation in img.getexif():
        orientation_value = exif[orientation]

        # Rotate image based on Exif orientation value
        if orientation_value == 3:
            img = img.rotate(180, expand=True)
        elif orientation_value == 6:
            img = img.rotate(270, expand=True)
        elif orientation_value == 8:
            img = img.rotate(90, expand=True)
        exif[orientation] = 1

    output = io.BytesIO()
    img.save(output, format=original_format, exif=exif.tobytes())
    output.seek(0)
    return output
