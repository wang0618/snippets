import shutil
from contextlib import contextmanager
from os import path, makedirs
from random import choice
from string import ascii_lowercase



@contextmanager
def tmp_dir(base=None):
    if base is None:
        here = path.dirname(path.abspath(__file__))
        base = path.join(here, '_tmp', random_str(10))
        makedirs(base, exist_ok=True)
        try:
            yield base
        finally:
            shutil.rmtree(base)
