#!/usr/bin/env python3

# dirty boy importing things from the parent :(
from sys import path
from os.path import join as path_join

path.insert(1, path_join(path[0], ".."))


from argparse import Namespace
from common import parse_file, parse_single_named_file_cli
from typing import List


def find_increasing_depths(depths: List[int]) -> int:
    total_increased = 0
    previous_depth = depths[0]

    for depth in depths[1:]:
        if depth > previous_depth:
            total_increased += 1
        previous_depth = depth

    return total_increased


def main(cli_args: Namespace):
    chall_txt = parse_file(cli_args.chall_input).strip().split("\n")
    chall_txt = list(map(int, chall_txt))
    print(find_increasing_depths(chall_txt))


if __name__ == "__main__":
    main(parse_single_named_file_cli())
