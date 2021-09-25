from PIL import Image


def scale_size(size, factor):
    return ((size[0] // factor), (size[1] // factor))


def image_resizer(imgfile):
    # read the image
    img = Image.open(imgfile)

    size = img.size

    # reduce size by half
    size = scale_size(size, 2)

    # resize image
    img = img.resize(size)

    # save resized image
    img.save('resize-output.jpg', quality=85)

    make_thumbnail(img)


def make_thumbnail(img: Image):

    # reduce size by half
    size = scale_size(img.size, 2)
    img = img.resize(size)

    box = (0, 0, size[1], size[1])
    size = (size[1], size[1])
    img = img.resize(size, box=box)
    img.save('resize-thumb.jpg', quality=85)


if __name__ == "__main__":
    image_resizer("images/IMG_1316.jpg")
