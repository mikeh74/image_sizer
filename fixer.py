import os
import sys

from PIL import Image


def scale_size(size, factor):
    return ((size[0] // factor), (size[1] // factor))


def save_image(img: Image, filename: str, quality: int = 85):
    path = os.path.join('output', filename)
    img.save(path, quality=85)


def image_resizer(imgfile):
    # read the image
    img = Image.open(imgfile)

    pieces = os.path.split(imgfile)
    filename = os.path.splitext(pieces[1])[0]

    save_image(
        make_resized(img),
        "{}_md.jpg".format(filename))

    save_image(
        make_thumbnail(img),
        "{}_thumb.jpg".format(filename),
        70
    )


def make_resized(img: Image):
    size = img.size

    # reduce size by half
    size = scale_size(size, 2)

    # resize image
    return img.resize(size)


def make_thumbnail(img: Image):

    # reduce size by half
    size = scale_size(img.size, 2)
    img = img.resize(size)

    box = (0, 0, size[1], size[1])
    size = (size[1], size[1])
    return img.resize(size, box=box)


if __name__ == "__main__":
    image_path = sys.argv[1]

    # image_path = 'images/IMG_1330.jpg'
    if os.path.exists(image_path):
        image_resizer(image_path)
    else:
        raise Exception('Path doesn\'t exist')
