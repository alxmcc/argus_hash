#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: github.com/alxmcc
"""

import hashlib
import re
import argparse


def match_header(file_header, regex_header):
    return True if regex_header.match(file_header) else False


def md5_hash(content):
    m = hashlib.md5()
    m.update(content)
    return m.hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Excludes Argus header/footer information and hashes content.")
    parser.add_argument('input', nargs='+', help='Input filename(s).')
    args = parser.parse_args()
    argus_dict = {}
    argus_header = re.compile(b'\x83\x10\x00\x20\x00{4}\xE5\x71\x2D\xCB[\x00-\xFF]{112}\xFF{4}')
    argus_footer = re.compile(b'\x83\x30\x00\x20\x00{20}[\x00-\xFF]{100}\xFF{4}')

    for argus_file in args.input:
        try:
            with open(argus_file, 'rb') as f:
                if match_header(f.read(128), argus_header):
                    f.seek(0)
                    data = f.read()
                    full_hash = md5_hash(data)
                    for header in re.finditer(argus_header, data):
                        head_slice = data[header.end():]
                        for footer in re.finditer(argus_footer, head_slice):
                            content = head_slice[:footer.start()]
                        break  # only want first header match and last footer match
                    argus_dict[argus_file] = [full_hash, md5_hash(content)]
                else:
                    print(argus_file, 'is not a Argus binary. Skipping.')
                    continue

        except (IsADirectoryError, FileNotFoundError, IOError):
            print(argus_file, 'not a valid file or file not found. Skipping.')
            continue
    if argus_dict:
        print('\n{: <44} {: <34} {}'.format('Filename', 'Full MD5', 'Content MD5'))
        for k, v in argus_dict.items():
            print('{: <44} {: <34} {}'.format(k, v[0], v[1]))
    else:
        print('No Argus binary files found.')


if __name__ == "__main__":
    main()
