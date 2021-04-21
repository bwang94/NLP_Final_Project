import time
start = time.perf_counter()
import re
import os
from collections import Counter
import pandas as pd
from os import path


# Define functions and variables
def create_regex(file):
    contents = pd.read_csv(file, sep=',', header=None, escapechar='\\')
    rgx = re.compile(r'\b(%s)\b' % '|'.join(contents[0].tolist()), re.IGNORECASE | re.MULTILINE)
    return rgx


def counter_to_csv(filename, cnt, enc='utf-8', direc=os.getcwd()):
    os.chdir(direc)
    if not path.exists(filename):
        with open(filename, 'x', encoding=enc) as newfile:
            for key, value in cnt.items():
                print(key, ',', value, file=newfile)


# To run code, replace regex_dir with the directory the drugs_regex.csv file is located in
regex_dir = r'C:\Users\brian\Desktop\drugs_regex.csv'

# Put test data through regex. Update test_dir to where the test files are located in
test_dir = r'C:\Users\brian\Desktop\Final Project Dataset - Divided\Test Data'

# Iterate through files in directory to put through baseline regex system
regex = create_regex(regex_dir)
os.chdir(test_dir)
matches = pd.DataFrame(columns=['File', 'MedicationMatches'])
for filename in os.listdir(test_dir):
    with open(filename, 'r') as file:
        temp = file.read().replace('\n', ' ')
    results = list(map(lambda m: tuple(filter(bool, m)), re.findall(regex, temp)))
    for index in range(len(results)):
        results[index] = results[index][0]
    # Add all matches to a pandas DataFrame
    matches = matches.append({'File': filename, 'MedicationMatches': results}, ignore_index=True)
print(matches)
counts = Counter()
for files in range(len(matches['MedicationMatches'])):
    for words in range(len(matches['MedicationMatches'][files])):
        counts.update(matches['MedicationMatches'][files][words].lower().split())
counter_to_csv(filename='regex_matches.csv', cnt=counts, direc=test_dir)
endtime = time.perf_counter()
print(endtime - start)

# TEST for 1 file
# with open('815850.txt','r') as file:
#    test = file.read().replace('\n', ' ')
# results = list(map(lambda m: tuple(filter(bool, m)), re.findall(rgx,test)))
# for index in range(len(results)):
#     temp = results[index][0]
#     results[index] = temp
# print(results)
