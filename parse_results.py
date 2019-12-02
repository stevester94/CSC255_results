#! /usr/bin/python3
import json
import sys
import pprint

pp = pprint.PrettyPrinter()

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        res = json.load(f)
print("res has the results list")
print("pp.pprint(__)")

