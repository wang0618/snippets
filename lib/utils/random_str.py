from random import choice
from string import ascii_lowercase


def random_str(length):
    return ''.join(choice(ascii_lowercase) for _ in range(length))
