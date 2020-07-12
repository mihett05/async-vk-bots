import argparse
from .startapp import startapp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("script_name", type=str)
    parser.add_argument("args", nargs="*")
    script_name = parser.parse_args().script_name
    args = parser.parse_args().args
    if script_name == "startapp":
        startapp(*args)


