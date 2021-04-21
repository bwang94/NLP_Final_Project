import os
from collections import Counter
from os import path
import re


def counter_to_csv(filename, cnt, enc='utf-8', direc=os.getcwd()):
    os.chdir(direc)
    if not path.exists(filename):
        with open(filename, 'x', encoding=enc) as newfile:
            for key, value in cnt.items():
                print(key, ',', value, file=newfile)


# Define functions and variables
def substring_after(s, delim):
    return s.partition(delim)[2]


def substring_after_n_occur(s, d, occur):
    return d.join(s.split(d)[occur:])


file_dir = r'C:\Users\bwang\Desktop'
count = Counter()
filename = r'MetamapRawCounts.csv'
os.chdir(file_dir)

with open(filename, 'r', encoding='utf-8') as file:
    results = file.read().split('\n')
    print(results)
for sent in results:
    newsent = sent.lower()
    trim1 = substring_after_n_occur(newsent, '|', 2)
    med = trim1.split('|')[0]
    count.update(med.split(' \n'))
counter_to_csv(filename='metamap_matches.csv', cnt=count, direc=file_dir)
