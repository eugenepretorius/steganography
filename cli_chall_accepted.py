# !/usr/bin/env python3

import argparse
import encode
import decode

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Steganography: Hiding an image inside another")

    parser.add_argument(
        '--decode',
        type=argparse.FileType('r', encoding='UTF-8'),
        required=False)

    parser.add_argument(
        '--encode',
        type=argparse.FileType('r', encoding='UTF-8'),
        required=False)

    parser.add_argument(
        '--msg',
        type=argparse.FileType('r', encoding='UTF-8'),
        required=False)

    parser.add_argument(
        '--bin',
        type=argparse.FileType('r', encoding='UTF-8'),
        required=False)

    parser.add_argument(
        '--out',
        required=False)

    args = parser.parse_args()

    if args.decode:
        args.decode.close()
        print(" please wait ... processing ... ")
        decode.unravel(args.decode.name)

    if args.encode and args.msg:
        args.encode.close()
        args.msg.close()
        args.bin.close()

        print(" please wait ... processing ... ")

        encode.merge_image(
            args.encode.name,
            args.msg.name,
            args.out)

        print("merge done")

        encode.add_hidden_text(
            args.out,
            args.bin.name,
            args.out
        )
        print("encoding done")
