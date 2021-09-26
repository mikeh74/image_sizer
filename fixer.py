import os

from PIL import Image


def scale_size(size, factor):
    return ((size[0] // factor), (size[1] // factor))


def save_image(img: Image, filename: str, outfile: str, quality: int = 85):
    path = os.path.join(outfile, filename)
    img.save(path, quality=quality)


def image_resizer(imgfile: str, outfile: str):
    # read the image
    img = Image.open(imgfile)

    pieces = os.path.split(imgfile)
    filename = os.path.splitext(pieces[1])[0]

    save_image(
        make_resized(img),
        "{}_md.jpg".format(filename),
        outfile
        )

    save_image(
        make_thumbnail(img),
        "{}_sq_thumb.jpg".format(filename),
        outfile,
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
    box = (
      start_x, 0,
      start_x + size[1],
      size[1])
    return img.crop(box)


def image_process_directory(directory: str, outfile: str):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            if os.path.splitext(f)[1] == '.jpg':
                image_resizer(f, outfile)


if __name__ == "__main__":

    import argparse

    # Create the parser
    arg_parser = argparse.ArgumentParser(
        prog='Image Resizer',
        usage='%(prog)s [options] file',
        description='Resize images in a folder')

    # Add the arguments
    arg_parser.add_argument(
        'Path',
        metavar='path',
        type=str,
        help='the path to directory or image')

    arg_parser.add_argument(
        '-o',
        metavar='output',
        dest='output',
        type=str,
        help='output path',
        default='')

    # Execute the parse_args() method
    args = arg_parser.parse_args()

    image_path = args.Path
    output_path = args.output

    if os.path.exists(image_path):

        if os.path.isdir(output_path) is False:
            # output_path = 'output'
            if os.path.isfile(image_path):
                output_path = os.path.split(image_path)[0]
            elif os.path.isdir(image_path):
                output_path = image_path

        if os.path.isfile(image_path):
            image_resizer(image_path, output_path)

        if os.path.isdir(image_path):
            image_process_directory(image_path, output_path)

    else:
        raise Exception('Path doesn\'t exist')
