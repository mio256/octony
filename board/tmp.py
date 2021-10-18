import csv
from os import read
import pprint

with open('board/ngword.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        for word in row:
            print(word)
