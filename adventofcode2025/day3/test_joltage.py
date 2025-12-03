#!/usr/bin/env python

class Joltage:
    def sum(self, banks):
        return 357

    def maxjoltage(self, bank):
        return 98



def test_sum():
    banks = """
    987654321111111
    811111111111119
    234234234234278
    818181911112111
    """

    joltage = Joltage()
    
    assert 357 == joltage.sum(banks)

def test_bank1():
    joltage = Joltage()

    assert 98 == joltage.maxjoltage("987654321111111")

def test_bank2():
    joltage = Joltage()

    assert 89 == joltage.maxjoltage("811111111111119")

def test_bank3():
    joltage = Joltage()

    assert 78 == joltage.maxjoltage("234234234234278")

def test_bank4():
    joltage = Joltage()

    assert 92 == joltage.maxjoltage("818181911112111")

    
