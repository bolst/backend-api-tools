import os
import json
import base64
import cv2
import numpy as np

CWD = os.path.dirname(os.path.realpath(__file__)) # get path to file relative to exec dir

def unique_filename(filename: str) -> str:
    path = os.path.join(CWD, filename)

    fileext = '.' + filename.split('.')[-1]

    retval = filename
    idx = 1
    while os.path.exists(retval):
        tag = '(' + str(idx) + ')'
        idx += 1
        retval = filename.replace(fileext, tag + fileext)

    return retval


# to get json data from a file
def read_json(filename: str):
    path = os.path.join(CWD, filename)

    if not os.path.isfile(path):
        raise Exception('File does not exist')

    with open(path, 'r') as f:
        return json.load(f)

# to dump json data to a file
# to create a new file if the file doesn't exist, make_new=True
def save_json(filename: str, data: dict, make_new=False):
    filename = unique_filename(filename)

    path = os.path.join(CWD, filename)

    if not make_new and not os.path.isfile(path):
        raise Exception('File does not exist')

    with open(path, 'w') as f:
        json.dump(data, f)

# to get an image file and return it as a string encoded in base64
def read_image(filename: str) -> str:
    path = os.path.join(CWD, filename)

    if not os.path.isfile(path):
        raise Exception('File does not exist')

    with open(path, 'rb') as image:
        f = image.read()
        return base64.b64encode(f).decode('utf-8')

# to save an image from a string of bytes and return the new filename
def save_image(filename: str, b64str: str) -> str:
    path = os.path.join(CWD, filename)

    nparr = np.fromstring(b64str, np.uint8)

    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # make filename unique
    filename = unique_filename(filename)

    cv2.imwrite(filename, img)

    return filename
