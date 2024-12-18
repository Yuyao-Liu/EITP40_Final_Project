import csv

input_file = '9.csv'

with open(input_file, 'r', newline='') as infile:
    reader = csv.reader(infile)
    rows = list(reader)
    
    rows.insert(1200, [])
    
    with open(input_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)
