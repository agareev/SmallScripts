import glob
import os

import shutil

root = os.path.expanduser("~") + "/Downloads"
path = root + "/Picture"
img_extention = ('jpg', 'gif', 'png', 'jpeg')


def find_img(root):
    os.chdir(root)
    img_paths = []
    for extention in img_extention:
        for file in glob.glob("*.{}".format(extention)):
            img_paths.append("{}/{}".format(root, file))
    return img_paths


def move_img(source, path=path):
    shutil.move(source, path)


if __name__ == "__main__":
    for image in find_img(root):
        move_img(image, path)
