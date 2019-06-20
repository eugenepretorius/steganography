import cv2
import numpy as np

def merge_image(im_src, im_msg, im_out="./data/merge.1.bmp"):
    src = cv2.imread(im_src, cv2.IMREAD_GRAYSCALE)
    msg = cv2.imread(im_msg, cv2.IMREAD_GRAYSCALE)

    if msg.shape[0] > src.shape[0] or \
       msg.shape[1] > src.shape[1]:
        print(src.shape)
        print(msg.shape)
        raise ValueError('Image 1 size is lower than image 2 size!')

    out = np.zeros(src.shape, dtype=np.uint8)
    for y in range(0, src.shape[0]):
        for x in range(0, src.shape[1]):
            # not doing a too complicated merge here for simplicity;
            # just dropping the 3 msb
            out[y, x] = np.uint8(
                (src[y, x] & 0xFF) |
                (msg[y, x] >> 3 & 0x1F))
            # prepare the lsb of image for adding text
            out[y, x] &= 0xFE
    cv2.imwrite(im_out, out)


def add_hidden_text(im_src, file_bin, im_out="./data/merge.2.bmp"):
    src = cv2.imread(im_src, cv2.IMREAD_GRAYSCALE)
    if src is None:
        raise ValueError("Could not load image: {}".format(im_src))

    out = src.copy()
    ylim = src.shape[0]
    line_cnt = 0

    with open(file_bin, "r") as fd_bin:
        for line in fd_bin:
            print(line)
            # check that the bin line fits in y-image space.
            if line_cnt >= ylim:
                break

            # check that bin line fits in x-image space
            num_bits = len(line) * 8
            if num_bits < src.shape[1]:
                line_cnt += 1

            y = line_cnt
            x = 0
            for k, c in enumerate(line):
                bits = np.unpackbits(np.array(ord(c), dtype=np.uint8))
                x = k * 8
                for i, b in enumerate(bits):
                    out[y, x + i] |= b

    cv2.imwrite(im_out, out)


# TODO: some utility functions i should clean up
# # add lines
# i = 0
# with open("data/homer-out.txt", "w") as fd:
#     with open("data/homer.txt", "r") as fd_in:
#         for line in fd_in:
#             z = "LINE{}.{}{}".format(i, line, "\n")
#             fd.write(z)
#             i += 1

# convert image to grayscale


def make_gray(im_file):
    img = cv2.imread(im_file, cv2.IMREAD_GRAYSCALE)
    print(img.shape)
    # newimg = cv2.resize(img, (int(img.shape[0]/3), int(img.shape[1]/3)))
    cv2.imwrite( "./data/out.bmp", img)
