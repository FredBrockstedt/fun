#!/usr/bin/env python

class Joltage:
    def sum(self, banks):
        return 357


def test_sum():
    banks = """
    987654321111111
    811111111111119
    234234234234278
    818181911112111
    """
    joltage = Joltage()
    
    assert 357 == joltage.sum(banks)

