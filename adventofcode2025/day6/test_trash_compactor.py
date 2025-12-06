#!/usr/bin/env python
# -*- coding: utf-8 -*-

# run this script with: ptw -c -w

import pytest

from collections import deque
from functools import reduce
import operator

def calc(data):
    stacks = []
    tally  = 0

    if isinstance(data, str):
        data = data.splitlines()

    for linecount, line in enumerate(data):
        line = line.split(" ")
        column = 0
        for item in line:
            if item.isdigit():
                if linecount == 0:
                    stacks.append([])

                stacks[column].append(int(item))
                column += 1

            if item == "+":
                tally += reduce(operator.add, stacks[column])
                column += 1

            if item == "*":
                tally += reduce(operator.mul, stacks[column])
                column += 1

    return tally


def right_to_left_in_columns(data):
    """
    Cephalopod math is written right-to-left in columns. Each number is given in its own column,
    with the most significant digit at the top and the least significant digit at the bottom.
    """

    if isinstance(data, str):
        data = data.splitlines()

    rows    = len(data)
    columns = len(data[0])

    # right to left
    for col in range(columns-1, -1, -1):
        # top to bottom
        stack = ""
        for row in range(0, rows):
            #print(f"{row} x {col}")
            stack += data[row][col].strip(" ")
        yield stack

def calc2(data):
    tally = 0
    items = list(right_to_left_in_columns(data))

    stack = []

    for item in items:

        if item.isdigit():
            stack.append(int(item))

        if item.endswith("+"):
            item = item.rstrip("+") 
            stack.append(int(item))
            tally += reduce(operator.add, stack)
            stack = []

        if item.endswith("*"):
            item = item.rstrip("*")
            stack.append(int(item))
            tally += reduce(operator.mul, stack)
            stack = []

    return tally

################################################################################
# pytest
@pytest.fixture
def data():
    return """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """

def test_part1(data):
    assert calc(data) == 4277556

def test_part2(data):
    data = data.splitlines()
    assert calc2(data) == 3263827

#def test_r2lcol():
#    assert list(right_to_left_in_columns("abcde")) == ["edcba"]

################################################################################
# main
if __name__ == '__main__':

    print("* Part 1")
    with open("data.txt", "r") as f:
        lines = f.read()

    s = calc(lines)
    print(f"Sum = {s}")

    print("* Part 2 ")
    s = calc2(lines.splitlines())
    print(f"Sum = {s}")
