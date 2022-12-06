from __future__ import annotations

import argparse
from typing import Sequence


def _fix_file(filename: str, max_blank_line_count: int) -> bool:
    with open(filename, mode='rb') as file_processed:
        lines = file_processed.readlines()

    modified = False
    blank_line_count = 0
    for i in range(len(lines)):
        if lines[i] == b'\n' or lines[i] == b'\r\n':
            blank_line_count += 1
        else:
            blank_line_count = 0
        if blank_line_count > max_blank_line_count:
            lines[i] = b''
            modified = True

    if modified:
        with open(filename, mode='wb') as file_processed:
            for line in lines:
                file_processed.write(line)
    return modified


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    parser.add_argument(
        '--max-blank-lines', type=int, default=1,
        help='Maximum allowable number of blank lines',
    )
    args = parser.parse_args(argv)

    return_code = 0
    for filename in args.filenames:
        if _fix_file(filename, args.max_blank_lines):
            print(f'Fixing {filename}')
            return_code = 1
    return return_code


if __name__ == '__main__':
    raise SystemExit(main())
