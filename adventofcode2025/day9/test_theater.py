import pytest

import logging
logging.basicConfig(encoding='utf-8', level=logging.INFO)


def square(data):
    """
    Return the largest sqaure
    """

    data = [line.split(',') for line in data.splitlines()]

    largest_square = 0
    largest_a = 0
    largest_b = 0
    
    for aidx, a in enumerate(data[:-1]):
        logging.info(f"* {aidx} - a = {a}")
        for b in data[1+aidx:]:
            s = (1+abs(int(a[0]) - int(b[0]))) * (1+abs(int(a[1]) - int(b[1])))

            logging.info(f"      b = {b} and s = {s}")

            if s > largest_square:
                largest_a = a
                largest_b = b
                largest_square = s

    return largest_square

@pytest.fixture
def data():
    return """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""


def test_square(data):

    # Ultimately, the largest rectangle you can make in this example has area 50. One way to do this is between 2,5 and 11,1
    assert 50 == square(data)

def main():
    print("* Part 1")
    with open("data.txt", encoding="utf-8", mode="r") as datafile:
        data = datafile.read()

    s = square(data)
    print(f"Square for part 1 = {s}")

if __name__ == '__main__':
    main()
