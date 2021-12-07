#!/usr/bin/env python3.10
# dirty boy importing things from the parent :(
from sys import exit, path
from os.path import join as path_join

path.insert(1, path_join(path[0], ".."))

from argparse import Namespace
from common import parse_file, parse_single_named_file_cli
from typing import List, Tuple


def handle_commands(commands: List[str], x_cord: int, y_cord: int) -> Tuple[int, int]:
    """Take a list of instructions and move a point along X,Y coordinates accordingly.

    Args:
        commands (List[str]): The set of commands in the form "_command_ _movement_"; where command
            is either forward, up, or down, and movement is an integer representing the amount
            to move.
        x_cord (int): The initial location of the X coordinate
        y_cord (int): The initial location of the Y coordinate
    """
    for command in commands:
        command, movement = command.split()
        match command:
            case "forward":
                x_cord += int(movement)
            case "up":
                y_cord -= int(movement)
            case "down":
                y_cord += int(movement)
            case _:
                print("Uh, you OK capt'n?")
                exit(1)

    return x_cord, y_cord


def main(cli_args: Namespace):
    chall_txt = parse_file(cli_args.chall_input).strip().split("\n")
    x, y = handle_commands(chall_txt, 0, 0)
    print(f"Day 2 part 1: {x*y}")


if __name__ == "__main__":
    main(parse_single_named_file_cli())
