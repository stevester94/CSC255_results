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
print('pp.pprint( [e for e in res if e["Protocol"] == "tcp" and "short" in e["Test Name"]])')
print('pp.pprint( [e for e in res if e["Protocol"] == "tcp" and "GIMP" in e["Test Name"]])')

