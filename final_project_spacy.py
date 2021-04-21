import time
start = time.perf_counter()
import scispacy
from scispacy.linking import EntityLinker
import spacy
from spacy.tokens import Doc, DocBin
import os
from os import path
import sys
from collections import Counter


# Define functions and variables
def substring_after(s, delim):
    return s.partition(delim)[2]


def counter_to_csv(filename, cnt, enc='utf-8', direc=os.getcwd()):
    os.chdir(direc)
    if not path.exists(filename):
        with open(filename, 'x', encoding=enc) as newfile:
            for key, value in cnt.items():
                print(key, ',', value, file=newfile)


train_dir = r'C:\Users\bwang\Desktop\Final Project Dataset - Divided\Training Data'
dev_dir = r'C:\Users\bwang\Desktop\Final Project Dataset - Divided\Dev Data'
test_dir = r'C:\Users\bwang\Desktop\Final Project Dataset - Divided\Test Data'
rxnorm_res = r'C:\Users\bwang\Desktop\Final Project Dataset - Divided\Test Results\RxNorm'
rxnorm_t_res = r'C:\Users\bwang\Desktop\Final Project Dataset - Divided\Test Results\RxNorm - Trained'
umls_res = r'C:\Users\bwang\Desktop\Final Project Dataset - Divided\Test Results\UMLS'

# Load scispaCy model and process the gold standard RXNorm data
realstart = time.perf_counter()
nlp_rxnorm = spacy.load("en_core_sci_lg")
print("Loaded scispaCy model 1")
rx1 = time.perf_counter()
# nlp_umls = spacy.load("en_core_sci_lg")
# umls1 = time.perf_counter()
# print("Loaded scispaCy model 2")
rxnorm = nlp_rxnorm.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "rxnorm"})
print("Rxnorm entity linker added")
rx2 = time.perf_counter()
# umls = nlp_umls.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "umls"})
# print("UMLS entity linker added")
# umls2 = time.perf_counter()

# Generate training data files
os.chdir(train_dir)
if not path.exists('TrainDataRXNORM.spacy'):
    rxnorm_bin = DocBin()
    # umls_bin = DocBin()
    for filename in os.listdir(train_dir):
        with open(filename, 'r') as file:
            traindata = file.read()
        rxnorm_doc = nlp_rxnorm(traindata)
        print("Generated rxnorm doc for", filename)
        # umls_doc = nlp_umls(traindata)
        # print("Generated UMLS doc for", filename)
        rxnorm_bin.add(rxnorm_doc)
        # umls_bin.add(umls_doc)
    rxnorm_bin.to_disk("./TrainDataRXNORM.spacy")
    # umls_bin.to_disk("./TrainDataUMLS.spacy")
t3 = time.perf_counter()

# Generate dev data files
os.chdir(dev_dir)
if not path.exists('DevDataRXNORM.spacy'):
    rxnorm_devbin = DocBin()
    # umls_devbin = DocBin()
    for filename in os.listdir(dev_dir):
        with open(filename, 'r') as file:
            devdata = file.read()
        rxnorm_doc = nlp_rxnorm(devdata)
        print("Generated rxnorm doc for", filename)
        # umls_doc = nlp_umls(devdata)
        # print("Generated UMLS doc for", filename)
        rxnorm_devbin.add(rxnorm_doc)
        # umls_devbin.add(umls_doc)
    rxnorm_devbin.to_disk("./DevDataRXNORM.spacy")
    # umls_devbin.to_disk("./DevDataRXNORM.spacy")
t4 = time.perf_counter()

## NOTE - the spaCy train command was run via command line at this point.
# Best trained pipeline now loaded

train_pipe_dir = r'C:\Users\bwang\OneDrive\Documents\Grad School\[2] Spring 2021\Natural Language Processing\FINAL'
os.chdir(train_pipe_dir)
nlp_trained = spacy.load('output/model-best')
rxnorm_trained = nlp_trained.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "rxnorm"})
print("Rxnorm entity linker added")

# Run on test data
os.chdir(test_dir)
if len(os.listdir(rxnorm_res)) == 0 and len(os.listdir(umls_res)) == 0 and len(os.listdir(rxnorm_t_res)) == 0:
    for filename in os.listdir(test_dir):
        os.chdir(test_dir)
        with open(filename, 'r') as file:
            testdata = file.read()
        rxnorm_doc = nlp_rxnorm(testdata)
        rxnorm_t_doc = nlp_trained(testdata)
        # umls_doc = nlp_umls(testdata)
        rxnorm_ents = rxnorm_doc.ents
        rxnorm_t_ents = rxnorm_t_doc.ents
        # umls_ents = umls_doc.ents
        rxnorm_file = filename[0:-4] + "_rxnorm.txt"
        rxnorm_t_file = filename[0:-4] + "_trained.txt"
        # umls_file = filename[0:-4] + "_umls.txt"
        os.chdir(rxnorm_res)
        with open(rxnorm_file, 'x', encoding='utf-8') as newfile:
            for ent in range(len(rxnorm_ents)):
                for rxnorm_ent in rxnorm_ents[ent]._.kb_ents:
                    print(rxnorm.kb.cui_to_entity[rxnorm_ent[0]], file=newfile)
        print(rxnorm_file, ' generated')
        os.chdir(rxnorm_t_res)
        with open(rxnorm_t_file, 'x', encoding='utf-8') as newfile:
            for ent in range(len(rxnorm_t_ents)):
                for rxnorm_t_ent in rxnorm_t_ents[ent]._.kb_ents:
                    print(rxnorm_trained.kb.cui_to_entity[rxnorm_t_ent[0]], file=newfile)
        print(rxnorm_t_file, ' generated')
        # os.chdir(umls_res)
        # with open(umls_file, 'x', encoding='utf-8') as newfile2:
        #     for ent in range(len(umls_ents)):
        #         for umls_ent in umls_ents[ent]._.kb_ents:
        #             print(umls.kb.cui_to_entity[umls_ent[0]], file=newfile2)
        # print(umls_file, ' generated')
t5 = time.perf_counter()

# Examine output data for matches
keyword = 'Name: '
os.chdir(rxnorm_res)
rxnorm_matches = Counter()
for filename in os.listdir(rxnorm_res):
    with open(filename, 'r') as file:
        results = file.read().split('\n')
        for sent in results:
            if keyword in sent:
                rxnorm_matches.update(substring_after(sent, keyword).lower().split('\n'))
counter_to_csv(filename='scispacy_rxnorm_matches.csv', cnt=rxnorm_matches, direc=rxnorm_res)

os.chdir(rxnorm_t_res)
rxnorm_t_matches = Counter()
for filename in os.listdir(rxnorm_t_res):
    with open(filename, 'r') as file:
        results = file.read().split('\n')
        for sent in results:
            if keyword in sent:
                rxnorm_t_matches.update(substring_after(sent, keyword).lower().split('\n'))
counter_to_csv(filename='scispacy_trained_matches.csv', cnt=rxnorm_t_matches, direc=rxnorm_t_res)
rx6 = time.perf_counter()

# os.chdir(umls_res)
# umls_matches = Counter()
# for filename in os.listdir(umls_res):
#     with open(filename, 'r') as file:
#         results = file.read().split('\n')
#         for sent in results:
#             if keyword in sent:
#                 umls_matches.update(substring_after(sent, keyword).lower().split('\n'))
# counter_to_csv(filename='scispacy_umls_matches.csv', cnt=umls_matches, direc=umls_res)
# umls6 = time.perf_counter()

# tot = umls6 - start
# rxload = rx1 - realstart + rx2 - umls1
# umlsload = umls1 - rx1 + umls2 - rx2
# traintime = t3 - umls2
# devtime = t4 - t3
# testtime = t5 - t4
# matchtime = umls6 - t5
# print('Total time: ', tot)
# print('RxNorm pipeline load time: ', rxload)
# print('UMLS pipeline load time: ', umlsload)
# print('Train parse time: ', traintime)
# print('Dev parse time: ', devtime)
# print('Test parse time: ', testtime)
# print('Match parse time: ', matchtime)
