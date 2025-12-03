#!/usr/bin/env python

class Joltage:
    def sum(self, banks):
        "Return the sum of joltages produced by banks parameter"
        return sum([self.maxjoltage(bank) for bank in banks])

    def maxjoltage(self, bank):
        "Returns the maximum of joltage a bank of batteries can produce"

        # find the largest number aslong as it is not the last
        # and its position in the bank
        left = max(list(bank[:-1]))
        left_index = bank.index(str(left))

        # we want to find the second number
        right = max(list(bank[left_index+1:]))
        
        return 10 * int(left) + int(right)

################################################################################
# pytest

def test_sum():
    banks = "987654321111111\n811111111111119\n234234234234278\n818181911112111"


    joltage = Joltage()
    
    assert 357 == joltage.sum(banks.split("\n"))

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

    
################################################################################
# main

def main():
    with open("data.txt", "r") as f:
        lines = f.read().splitlines()

    j = Joltage()

    joltage = j.sum(lines)
    print(f"Joltage = {joltage}")

if __name__ == '__main__':
    main()
