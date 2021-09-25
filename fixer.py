from PIL import Image

# read the image
img = Image.open("images/IMG_1316.jpg")

size = img.size

# reduce size by half
size = ((size[0] // 2), (size[1] // 2))

# resize image
img = img.resize(size)

# save resized image
img.save('resize-output.jpg', quality=85)

# Create square version
start_x = (size[0] - size[1]) // 2

box = (0, 0, size[1], size[1])
size = (size[1], size[1])
img = img.resize(size, box=box)
img.save('resize-thumb.jpg', quality=85)
