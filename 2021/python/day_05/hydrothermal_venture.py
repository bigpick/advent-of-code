#!/usr/bin/env python3

# dirty boy importing things from the parent :(
from sys import path
from os.path import join as path_join

path.insert(1, path_join(path[0], ".."))

from argparse import Namespace
from common import parse_file, parse_single_named_file_cli


class LineSegment:
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self) -> str:
        return f"LineSegment( {self.y1},{self.x1} -> {self.y2},{self.x2} )"

    @classmethod
    def from_str(cls, coords: str) -> "LineSegment":
        """Create a LineSegment from a string.

        The string is assumed to be of the form

            "x1,y1 -> x2,y2"
        """
        first_point, second_point = [coord.split(",") for coord in coords.split(" -> ")]
        return LineSegment(
            int(first_point[1]),
            int(first_point[0]),
            int(second_point[1]),
            int(second_point[0]),
        )


class OceanFloor:
    def __init__(self) -> None:
        """Initialize a new OceanFloor object.

        This object will represent the OceanFloor containing the various
        thermal vents. It will take the form of a dictionary, such that
        the top level key are x coordinates, which contain another set
        keys representing y coordinates, which have a value representing
        the total number of vents running over the coordinate.
        """
        # Initialize an empty bed, such that it starts at (0,0), with
        # currently no lines within it.
        self.bed = {}

    def __str__(self) -> str:
        grid = []
        max_x = max(self.bed.keys())
        max_y_s = []
        for xrow in range(max_x + 1):
            try:
                max_y_s.append(max(self.bed[xrow].keys()))
            except KeyError:
                max_y_s.append(0)

        max_y = max(max_y_s)

        for xrow in range(max_x + 1):
            floorrow = ""
            for ycord in range(max_y + 1):
                overlaps = 0
                try:
                    overlaps = self.bed[xrow][ycord]
                except KeyError:
                    floorrow += "."
                    continue

                if overlaps == 0:
                    floorrow += "."
                else:
                    floorrow += str(overlaps)
            grid.append(floorrow)
        return "\n".join(grid)

    def _increment_point(self, xcoord: int, ycoord: int):
        try:
            self.bed[xcoord]
        except KeyError:
            self.bed[xcoord] = {}

        try:
            self.bed[xcoord][ycoord] += 1
        except KeyError:
            self.bed[xcoord][ycoord] = 1

    def add_segment(self, segment: LineSegment) -> None:
        xdiff = segment.x2 - segment.x1
        ydiff = segment.y2 - segment.y1
        if xdiff == ydiff == 0:
            self._increment_point(segment.x1, segment.y1)

        elif xdiff == 0:  # horizontal line
            if ydiff > 0:
                for ycoord in range(segment.y1, segment.y1 + ydiff + 1):
                    self._increment_point(segment.x1, ycoord)
            else:
                maxy = max(segment.y1, segment.y2)
                for ycoord in range(maxy, maxy + (ydiff - 1), -1):
                    self._increment_point(segment.x1, ycoord)
        elif ydiff == 0:  # vertical
            if xdiff > 0:
                for xcoord in range(segment.x1, segment.x1 + xdiff + 1):
                    self._increment_point(xcoord, segment.y1)
            else:
                maxx = max(segment.x1, segment.x2)
                for xcoord in range(maxx, maxx + (xdiff - 1), -1):
                    self._increment_point(xcoord, segment.y1)

        else:
            pass
            # print("Hey, you said only vertical and horizontal!")

    def find_total_overlapping(self) -> int:
        total = 0
        for x in self.bed.keys():
            for y in self.bed[x].keys():
                if self.bed[x][y] > 1:
                    total += 1
        return total


EXAMPLE = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""


def main(cli_args: Namespace):
    chall_txt = parse_file(cli_args.chall_input).strip().split("\n")
    segments = []
    for line in chall_txt:
        # for line in EXAMPLE.split("\n"):
        #    if line:
        segments.append(LineSegment.from_str(line.strip()))

    floor = OceanFloor()
    for segment in segments:
        floor.add_segment(segment)

    print(floor)
    #print(floor.find_total_overlapping())


if __name__ == "__main__":
    main(parse_single_named_file_cli())
