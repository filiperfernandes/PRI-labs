from collections import Counter
from collections import defaultdict

import spacy, sys, csv
import argparse

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load('en_core_web_sm')
csv.field_size_limit(sys.maxsize)
party_list = []
text_list = []
text_per_party_list = []
available_party_list = []
doc_dict={}
MAX = 1000000

party_dict = {}


def get_parser():
    parser = argparse.ArgumentParser(description="""PRI statistical analysis tool""")
    parser.add_argument('-f', '--file', dest='file', help="""receive file from stdin [default: no]""",
                        action="store")
    return parser


def magic():
    with open("../pri_project_data/en_docs_clean.csv", 'r') as f:
        # blocksize = 947778
        # text = f.read(blocksize)
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            party_list.append(row['party'])
            text_list.append(row['text'])
        count = 0

        # Populate Party List
        get_party_list(party_list)
        # Make dictionary with all texts per party
        for party in party_list:
            for cParty in available_party_list:
                if party == cParty and party is not None and party != "None":
                    party_dict.update({party: str(party_dict.get(party)) + " " + str(count)})
            count = count + 1

        for party in available_party_list:
            text = ""
            current_text_list = party_dict.get(party).split()
            for iid in current_text_list:
                if iid is None or iid == 'None':
                    continue
                else:
                    text += text_list[int(iid)]
                    doc_dict.update({party: text})

        # Get Most Named Entity Per Party
        get_most_named_entity_per_party()


def get_party_list(list_of_parties):
    for party in list_of_parties:
        if party not in available_party_list:
            available_party_list.append(party)


def get_entity_list(list_of_entities):
    entity_list = []
    for entity in list_of_entities.ents:
        entity_list.append(entity.label_)

    c = Counter(entity_list)
    return c.most_common(2)


def get_most_named_entity_per_party():
    # TODO: save it in a structure!!
    for party in available_party_list:
        ola = doc_dict.get(party)
        firstpart, secondpart = ola[:len(ola) // 2], ola[len(ola) // 2:]
        doc1 = nlp(firstpart)
        doc2 = nlp(secondpart)
        res1 = get_entity_list(doc1)
        res2 = get_entity_list(doc2)
        testDict = defaultdict(int)
        final_res = res1 + res2

        for key, val in final_res:
            testDict[key] += val

        # RES yelds most named entities for each party
        res = testDict.items()

        bigger = 0
        bigger_key = ""
        for key, val in res:
            if testDict[key] > bigger:
                bigger = testDict[key]
                bigger_key = key
        print(party + ":")
        print("Most named entity is: " + bigger_key + " occurs " + str(testDict[bigger_key]) + " times")



        # if res1[0][0] == res2[0][0]:
        #     final_res = [(res1[0][0], int(res1[0][1]) + int(res2[0][1]))]
        # elif res1[1][0] == res2[1][0]:
        #     final_res = [(res1[1][0], int(res1[1][1]) + int(res2[1][1]))]
        # elif res1[0][0] == res2[1][0]:
        #     final_res = [(res1[0][0], int(res1[0][1]) + int(res2[1][1]))]
        # elif res1[1][0] == res2[0][0]:
        #     final_res = [(res1[1][0], int(res1[1][1]) + int(res2[0][1]))]
        # else:
        #     print("TODO")
        # print(res1)
        # print(res2)
        # print(final_res)


def get_most_named_entity_globally():
    text_str = ""
    with open("../pri_project_data/en_docs_clean.csv", 'r') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            party_list.append(row['party'])
            text_list.append(row['text'])
        for text in text_list:
            if len(text_str) < (MAX - len(text)):
                text_str += text
            else:
                doc = nlp(text_str)
                res = get_entity_list(doc)
                print(res)
                text_str = ""


def count_entities(list_of_entities, entity_list):
    entity_count = {}
    for entity in list_of_entities.ents:
        if entity.label_ in entity_list:
            val = entity_count.get(entity.label_)
            if val is not None and val != {}:
                entity_count.update({entity.label_: val + 1})
            else:
                continue
    return entity_count


def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    file = args['file']

    if file:
        print("Using file " + file)
    else:
        magic()


if __name__ == "__main__":
    main()
    # get_most_named_entity_globally()

# doc = nlp(text)

# Find named entities, phrases and concepts
# for entity in doc.ents:
#    print(entity.text, entity.label_)
