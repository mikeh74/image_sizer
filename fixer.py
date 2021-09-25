import os
import sys

from PIL import Image


def scale_size(size, factor):
    return ((size[0] // factor), (size[1] // factor))


def image_resizer(imgfile):
    # read the image
    img = Image.open(imgfile)

    pieces = os.path.split(imgfile)
    filename = os.path.splitext(pieces[1])[0]

    make_resized(img, filename)
    make_thumbnail(img, filename)


def make_resized(img: Image, filename: str):
    size = img.size

    # reduce size by half
    size = scale_size(size, 2)

    # resize image
    img = img.resize(size)

    # save resized image
    img.save('{}_md.jpg'.format(filename), quality=85)


def make_thumbnail(img: Image, filename: str):

    # reduce size by half
    size = scale_size(img.size, 2)
    img = img.resize(size)

    box = (0, 0, size[1], size[1])
    size = (size[1], size[1])
    img = img.resize(size, box=box)
    img.save('{}_thumb.jpg'.format(filename), quality=85)


if __name__ == "__main__":
    # image_path = sys.argv[1]
    # image_resizer(image_path)

    image_path = 'images/IMG_1330.jpg'
    if os.path.exists(image_path):
        image_resizer(image_path)
    else:
        raise Exception('Path doesn\'t exist')
