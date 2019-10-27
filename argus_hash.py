#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: github.com/alxmcc
"""

import hashlib
import re
import os
import argparse


def argus_header(file_header):
    argus_header = re.compile(b'\x83\x10\x00\x20\00{4}\xE5\x71\x2D\xCB')
    return True if argus_header.match(file_header) else False


def md5_hash(content):
    m = hashlib.md5()
    m.update(content)
    return m.hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Excludes Argus header/footer information and hashes content.")
    parser.add_argument('input', nargs='+', help='Input filename(s).')
    args = parser.parse_args()
    argus_dict = {}

    for argus_file in args.input:
        try:
            with open(argus_file, 'rb') as f:
                if argus_header(f.read(12)):
                    f.seek(0)
                    full_hash = md5_hash(f.read())
                    f.seek(128)
                    data = f.read(os.path.getsize(argus_file) - 256)
                    argus_dict[argus_file] = [full_hash, md5_hash(data)]
                else:
                    print(argus_file, 'is not a Argus binary. Skipping.')
                    continue

        except IsADirectoryError:
            print(argus_file, 'is a directory. Skipping.')
            continue

    print('\n{: <40} {: <34} {}'.format('Filename', 'Full MD5', 'Content MD5'))
    for k, v in argus_dict.items():
        print('{: <40} {: <34} {}'.format(k, v[0], v[1]))


if __name__ == "__main__":
    main()
