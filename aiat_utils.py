import csv
import sys

def tryread(name):
    try:
        with open(name, "r", encoding="utf8") as csvfile:
            return [r for r in csv.reader(csvfile)]
    except:
        errexit(f"Could not read file: {name}", -1)

def errexit(msg, exit_code):
	print(msg, file=sys.stderr)
	exit(exit_code)