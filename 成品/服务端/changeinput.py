import cv2
from PIL import Image


def changes(filename=""):
    imc = cv2.imread(filename)
    cv2.imwrite(filename, imc)
    im = Image.open(filename)
    # print("h=",im.height,"w=",im.width)

    maxx = min(im.height, im.width)
    # box = (0, 0, maxx, maxx)
    # im = im.crop(box)
    if maxx > 450:
        im = im.resize((450, int(405 / (im.width / im.height))), Image.BICUBIC)
        im.save(filename, "JPEG", quality=100)
