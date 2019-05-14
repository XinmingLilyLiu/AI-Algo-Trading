import json
import sys

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: to_csv.py [file.json] c,o,l,s")
		exit(1)

	with open(sys.argv[1], "r") as f:
		obj = json.load(f)
		cols = sys.argv[2].split(",")
		
		data = obj['history']['day']
		
		print(sys.argv[2])
		
		for row in data:
			print(",".join([str(row[i]) for i in cols]))