#Script for converting a CSV file to JSON

import csv
import json
import argparse

def main():
	parser = argparse.ArgumentParser()
        parser.add_argument(
                "csv_file", help="CSV input file. The input file should have the fields 'Year', 'URL', 'News' in the same order", type=str)
        parser.add_argument(
                "json_file", help="JSON output file", type=str)

        args = parser.parse_args()
        f_csv_file = args.csv_file
        f_json_file = args.json_file

	#File pointer to input CSV file
	in_file = open(f_csv_file,"r")

 	#File pointer to output JSON file
	out_file = open(f_json_file,"w")

	#Read CSV file 
	reader1 = csv.DictReader(in_file, fieldnames=("Year", "URL", "News"))

	#Convert to JSON and write to output file
	converted_input = json.dumps([row for row in reader1], ensure_ascii=False, sort_keys=False, indent=4)
	out_file.write(converted_input)
	out_file.close()

if __name__ == '__main__':
	main()
