#!/usr/bin/env python3

# dirty boy importing things from the parent :(
from sys import path
from os.path import join as path_join

path.insert(1, path_join(path[0], ".."))


from argparse import Namespace
from common import parse_file, parse_single_named_file_cli
from typing import List


def find_increasing_depths(depths: List[int]) -> int:
    """Count the number of times a value is higher than its previous index's value.

    Args:
        depths (List[int]): The list of values to inspect.
    """
    total_increased = 0
    previous_depth = depths[0]

    for depth in depths[1:]:
        if depth > previous_depth:
            total_increased += 1
        previous_depth = depth

    return total_increased


def produce_windows(depths: List[int], window_size: int) -> List[List[int]]:
    """Create a set a sliding windows of specified size from a given list.

    Args:
        depths (List[int]): A list of values to produce the windows from.
        window_size (int): The size of windows to create.

    Returns:
        List[List[int]]: A list of windows, which are lists themselves containing
            `window_size` entries.
    """
    return [depths[i : i + window_size] for i in range(len(depths) - window_size + 1)]


def main(cli_args: Namespace):
    chall_txt = parse_file(cli_args.chall_input).strip().split("\n")
    chall_txt = list(map(int, chall_txt))
    print(f"Day 1: Part 1: {find_increasing_depths(chall_txt)}")

    window_sums = [sum(window) for window in produce_windows(chall_txt, 3)]
    print(f"Day 1: Part 2: {find_increasing_depths(window_sums)}")


if __name__ == "__main__":
    main(parse_single_named_file_cli())
