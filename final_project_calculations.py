from sklearn.metrics import precision_recall_fscore_support
import os

dir = r'C:\Users\bwang\Desktop\Final Project Dataset - Divided\Test Results'
os.chdir(dir)

with open(r'scispacy_rxnorm_matches.csv', 'r', encoding='utf-8') as file:
    reader = file.read().split('\n')
    rxnorm = list(reader)
print(rxnorm)

with open(r'scispacy_trained_matches.csv', 'r', encoding='utf-8') as file:
    reader = file.read().split('\n')
    trained = list(reader)
print(trained)

with open(r'gold_std_matches.csv', 'r', encoding='utf-8') as file:
    reader = file.read().split('\n')
    gold = list(reader)

with open(r'regex_matches.csv', 'r', encoding='utf-8') as file:
    reader = file.read().split('\n')
    regex = list(reader)

with open(r'metamap_matches.csv', 'r', encoding='utf-8') as file:
    reader = file.read().split('\n')
    mm = list(reader)
print(mm)

print(len(set(mm).intersection(set(rxnorm))))
print(len(set(mm) - set(rxnorm)))
print(len(set(rxnorm) - set(mm)))
print(len(set(mm).intersection(set(trained))))
print(len(set(mm) - set(trained)))
print(len(set(trained) - set(mm)))
print(len(set(rxnorm).intersection(set(trained))))
print(len(set(rxnorm) - set(trained)))
print(len(set(trained) - set(rxnorm)))

