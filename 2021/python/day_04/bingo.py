#!/usr/bin/env python3
from __future__ import annotations

# dirty boy importing things from the parent :(
from sys import path, exit
from os.path import join as path_join

path.insert(1, path_join(path[0], ".."))

from argparse import Namespace
from common import parse_file, parse_single_named_file_cli
from json import dumps
from typing import List, Optional, Tuple


class BingoSquare:
    def __init__(self, value: int = -1, marked: bool = False) -> None:
        self.box = {"value": value, "marked": marked}

    def __repr__(self) -> str:
        return dumps(self.__dict__)

    def __str__(self) -> str:
        return dumps(self.__dict__)

    def is_marked(self) -> bool:
        return self.box["marked"]

    def set_value(self, val: int) -> None:
        self.box["value"] = val

    def mark(self, val: int) -> None:
        if self.box["value"] == val:
            self.box["marked"] = True

    def get(self) -> dict[str, int | bool]:
        return self.box


class BingoCard:
    def __init__(self, rows: Optional[List[List[BingoSquare]]] = None):
        if not rows:
            self.card = [
                [BingoSquare()] * 5,
                [BingoSquare()] * 5,
                [BingoSquare()] * 5,
                [BingoSquare()] * 5,
                [BingoSquare()] * 5,
            ]
        else:
            self.card = rows

    def get_square(self, row: int, col: int) -> dict[str, int | bool]:
        return self.card[row][col].box

    def __str__(self) -> str:
        cardstr = "BingoCard(\n"
        for row in self.card:
            for idx, square in enumerate(row):
                sqr = square.get()
                cardstr += f"""({sqr["value"]}: {sqr["marked"]})"""
                if idx != len(row) - 1:
                    cardstr += ", "
            cardstr += "\n"
        return cardstr + ")"

    def mark(self, val: int) -> Tuple[bool, int]:
        """Attempt to mark a value off the card.

        Args:
            val (int): The value to search and mark off the card.

        Returns:
            Tuple[bool, int]: Whether or not the card has bingo after
                potentially marking off the value.
        """
        # Try to mark a num
        _ = [cardd.mark(val) for row in self.card for cardd in row]
        return self.has_bingo()

    def has_bingo(self) -> Tuple[bool, int]:
        """Check a card for any current bingos.

        Returns:
            Tuple[bool, int]: If found, returns True, and the sum of
                all UNCHECKED squares.
        """
        diagonalR = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]
        diagonalL = [[4, 0], [3, 1], [2, 2], [1, 3], [0, 4]]

        # check all rows / columns
        for row in range(5):
            if all(
                self.get_square(row, column)["marked"] == True for column in range(5)
            ) or all(
                self.get_square(column, row)["marked"] == True for column in range(5)
            ):
                return (True, self.sum_all_unchecked())

        # check diagonals
        if all(
            self.get_square(row, column)["marked"] == True for row, column in diagonalR
        ) or all(
            self.get_square(row, column)["marked"] == True for row, column in diagonalL
        ):
            return (True, self.sum_all_unchecked())

        return (False, -1)

    def sum_all_unchecked(self) -> int:
        """Return the sum of all unchecked bingo squares."""
        sum = 0
        for row in self.card:
            for card in row:
                box = card.get()
                sum += box["value"] if not box["marked"] else 0
        return sum

    @classmethod
    def from_str(cls, cardlines: List[str]) -> BingoCard:
        """Create a BingoCard object from a string dump.

        For example:

            22 13 17 11  0
            8  2 23  4 24
            21  9 14 16  7
            6 10  3 18  5
            1 12 20 15 19

        Args:
            cardlines (List[str]): a list of 5 lines each with 5 values
                representing the values to fill on the board
        """
        rows = []
        for cardrow in cardlines:
            rows.append([BingoSquare(int(val), False) for val in cardrow.split()])
        return BingoCard(rows)


# def find_first_bingo(
#    boards: List[BingoCard], picked_nums: List[int]
# ) -> Optional[Tuple[int, int, BingoCard]]:
#    for num in picked_nums:
#        for card in boards:
#            (bingo, score) = card.mark(num)
#            if bingo:
#                return score, num, card
#    return None


def find_all_bingos(
    boards: List[BingoCard], picked_nums: List[int]
) -> List[Tuple[int, int, BingoCard]]:
    bingos = []
    for num in picked_nums:
        for card in boards:
            (bingo, score) = card.mark(num)
            if bingo:
                boards.remove(card)
                bingos.append((score, num, card))
    return bingos


def main(cli_args: Namespace):
    chall_txt = parse_file(cli_args.chall_input).strip().split("\n")
    picked_nums = list(map(int, chall_txt[0].split(",")))

    chall_txt = [line for line in chall_txt[1:] if line != ""]
    boards = [chall_txt[i : i + 5] for i in range(0, len(chall_txt), 5)]

    cards = [BingoCard.from_str(board) for board in boards]
    bingos = find_all_bingos(cards, picked_nums)
    first_bingo = bingos[0]
    last_bingo = bingos[-1]

    print(
        f"First BINGO!!! Unmarked: {first_bingo[0]} || Last Drawn: {first_bingo[1]} || Score: {first_bingo[0]*first_bingo[1]}"
    )
    print(
        f"Last BINGO!!! Unmarked: {last_bingo[0]} || Last Drawn: {last_bingo[1]} || Score: {last_bingo[0]*last_bingo[1]}"
    )


if __name__ == "__main__":
    main(parse_single_named_file_cli())
