#!/usr/bin/env python3

# dirty boy importing things from the parent :(
from sys import path
from os.path import join as path_join

path.insert(1, path_join(path[0], ".."))

from argparse import Namespace
from common import parse_file, parse_single_named_file_cli
from typing import List


def most_frequent_bit(binaries: List[str], idx: int) -> str:
    bit_counts = {"1": 0, "0": 0}
    for bits in binaries:
        bit_counts[bits[idx]] += 1
    if (bit_counts["1"] > bit_counts["0"]) or (bit_counts["1"] == bit_counts["0"]):
        return "1"
    else:
        return "0"


def least_frequent_bit(binaries: List[str], idx: int) -> str:
    mfb = most_frequent_bit(binaries, idx)
    return "0" if mfb == "1" else "1"


def main(cli_args: Namespace):
    chall_txt = parse_file(cli_args.chall_input).strip().split("\n")
    most_frequent_bits = [
        most_frequent_bit(chall_txt, idx) for idx, _ in enumerate(chall_txt[0])
    ]
    least_frequent_bits = ["1" if x == "0" else "0" for x in most_frequent_bits]

    gamma = "".join(most_frequent_bits)
    epsilon = "".join(least_frequent_bits)
    power_consumption = int(gamma, 2) * int(epsilon, 2)
    print(f"Day 3 part 1: {power_consumption}")

    most_frequent_bits = [
        most_frequent_bit(chall_txt, idx) for idx, _ in enumerate(chall_txt[0])
    ]
    least_frequent_bits = ["1" if x == "0" else "0" for x in most_frequent_bits]

    oxygen_gen = chall_txt
    for idx in range(len(chall_txt[0])):
        mfb = most_frequent_bit(oxygen_gen, idx)
        new = [reading for reading in oxygen_gen if reading[idx] == mfb]
        oxygen_gen = new if new else oxygen_gen

    carbon_mono = chall_txt
    for idx in range(len(chall_txt[0])):
        lfb = least_frequent_bit(carbon_mono, idx)
        new = [reading for reading in carbon_mono if reading[idx] == lfb]
        carbon_mono = new if new else carbon_mono

    life_supp_rating = int("".join(oxygen_gen), 2) * int("".join(carbon_mono), 2)
    print(f"Day 3 part 1: {life_supp_rating}")


if __name__ == "__main__":
    main(parse_single_named_file_cli())
