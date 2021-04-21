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


std_dir = r'C:\Users\bwang\Desktop\Final Project Dataset - Divided\Gold Standard Annotations'
count = Counter()

os.chdir(std_dir)
keyphrase = 'm=\"'
for filename in os.listdir(std_dir):
    with open(filename, 'r') as file:
        results = file.read().split('\" ')
    for sent in results:
        if keyphrase in sent:
            count.update(substring_after(sent, keyphrase).lower().split('\n'))
counter_to_csv(filename='gold_std_matches.csv', cnt=count, direc=std_dir)