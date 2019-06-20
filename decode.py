import cv2
from matplotlib import pyplot as plt
import numpy as np


def unravel(im_file, out_file="./data/decoded.txt"):
    img = cv2.imread(im_file, cv2.IMREAD_UNCHANGED)
    print(img.shape)

    cols = img.shape[0]
    z1 = np.zeros((cols, img.shape[1]), dtype=bool)
    z2 = np.zeros((cols, img.shape[1]))
    zn = np.zeros((cols, img.shape[1]//8), dtype=np.uint8)

    for y in range(0, cols):
        for x in range(0, img.shape[1]):
            z2[y, x] = int((np.uint8(img[y, x]) & 0x03) << 8)
            z1[y, x] = img[y, x] & 0x01 == 1

    for y in range(0, cols):
        row = ""
        for x in range(0, img.shape[1]//8):
            zn[y, x] = np.uint8(np.packbits(z1[y, x*8:x*8+8]))
            row += chr(zn[y, x])

        # HACKY way to handle the empty rows!
        if any(zn[y, :] != 0):
            print(row[0:-1])    # str end-1 to avoid encoded newline

            with open(out_file, "a") as fd:
                fd.write(row[0:-1])

    hist_full = cv2.calcHist([img], [0], None, [256], [0, 256])

    plt.figure()
    plt.subplot(231), plt.imshow(img, 'gray'), plt.axis('off'), plt.title("INPUT IMAGE")
    plt.subplot(232), plt.imshow(z2, 'gray'), plt.axis('off'), plt.title("HIDDEN IMAGE")
    plt.subplot(233), plt.imshow(z1, 'gray'), plt.axis('off'), plt.title("HIDDEN TEXT")
    plt.subplot(212), plt.plot(hist_full), plt.title("INPUT IMAGE HISTOGRAM")

    plt.show()
