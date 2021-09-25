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
        "{}_sq_thumb.jpg".format(filename),
        70
    )


def make_resized(img: Image):
    size = img.size

    factor = 2
    if size[0] > 1000:
        factor = size[0] // 1000

    # reduce size by half
    size = scale_size(size, factor)

    # resize image
    return img.resize(size)


def make_thumbnail(img: Image):

    factor = 2
    if img.size[0] > 1000:
        factor = img.size[0] // 1000

    # reduce size by half
    size = scale_size(img.size, (factor * 2))
    img = img.resize(size)

    start_x = (size[0] - size[1]) // 2

    box = (start_x, 0, size[1], size[1])
    size = (size[1], size[1])
    return img.resize(size, box=box)


def image_process_directory(directory: str):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            if os.path.splitext(f)[1] == '.jpg':
                image_resizer(f)


if __name__ == "__main__":
    image_path = sys.argv[1]
    # image_path = 'images/'

    if os.path.exists(image_path):

        if os.path.isfile(image_path):
            image_resizer(image_path)

        if os.path.isdir(image_path):
            image_process_directory(image_path)

    else:
        raise Exception('Path doesn\'t exist')
