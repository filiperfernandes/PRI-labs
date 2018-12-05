from collections import Counter
from collections import defaultdict

import spacy
import argparse
import sys
import csv

# Load English tokenizer, tagger, parser, NER and word vectors
MAX = 1000000
FILE_PATH = "../pri_project_data/pt_docs_clean.csv"
nlp = spacy.load('en_core_web_sm')
csv.field_size_limit(sys.maxsize)
party_list = []
text_list = []
text_per_party_list = []
available_party_list = []
doc_dict = {}
party_dict = {}


def get_parser():
    parser = argparse.ArgumentParser(description="""PRI statistical analysis tool""")
    parser.add_argument('-f', '--file', dest='file', help="""receive file from stdin [default: no]""",
                        action="store")
    parser.add_argument('-l', '--language', dest='language', help="""Specify language 'en' or 'pt'""",
                        action="store")
    parser.add_argument('-p', '--party', help="""What are the most mentioned entities for each party?""",
                        action="store_true")
    parser.add_argument('-g', '--globally', help="""What are the most mentioned entities globally?""",
                        action="store_true")
    parser.add_argument('-t', '--times', help="""How many times does any given party mention other parties?""",
                        action="store_true")
    parser.add_argument('-m', '--mention', help="""Which party is mentioned more times by the other parties?""",
                        action="store_true")
    return parser


def get_party_list(list_of_parties):
    for party in list_of_parties:
        if party not in available_party_list:
            available_party_list.append(party)


def get_entity_list(list_of_entities):
    entity_list = []
    for entity in list_of_entities.ents:
        entity_list.append(entity.label_)

    c = Counter(entity_list)
    return c.most_common(3)


def get_most_named_entity_per_party():

    with open(FILE_PATH, 'r') as f:
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

        # TODO: save it in a structure!! or not
        for party in available_party_list:
            ola = doc_dict.get(party)
            firstpart, secondpart = ola[:len(ola) // 2], ola[len(ola) // 2:]
            doc1 = nlp(firstpart)
            doc2 = nlp(secondpart)
            res1 = get_entity_list(doc1)
            res2 = get_entity_list(doc2)
            final_res = res1 + res2
            test_dict = defaultdict(int)

            for key, val in final_res:
                test_dict[key] += val

            # RES yelds most named entities for each party
            res = test_dict.items()
            print(party + ":")
            print("Top entities mentioned:")
            print(res)

            # bigger = 0
            # bigger_key = ""
            # for key, val in res:
            #     if testDict[key] > bigger:
            #         bigger = testDict[key]
            #         bigger_key = key
            # print(party + ":")
            # print("Most named entity is: " + bigger_key + " occurs " + str(testDict[bigger_key]) + " times")


def get_most_named_entity_globally():
    text_str = ""
    final_res = []
    with open(FILE_PATH, 'r') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            party_list.append(row['party'])
            text_list.append(row['text'])
        for text in text_list:
            if len(text_str) < (MAX - len(text)):
                text_str += text
            else:
                doc = nlp(text_str)
                final_res += get_entity_list(doc)
                text_str = ""

        test_dict = defaultdict(int)

        for key, val in final_res:
            test_dict[key] += val

        # RES yelds most named entities for each party
        res = test_dict.items()
        print("Top entities mentioned:")
        print(res)


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


def most_mentioned_party_per_party():

    with open(FILE_PATH, 'r') as f:
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

        # TODO: save it in a structure!! or not
        for party in available_party_list:
            ola = doc_dict.get(party)
            for counting in available_party_list:
                if party == counting:
                    continue
                else:
                    print(party + ' mentions ' + '"'+counting+'"' + ' (times):')
                    print(ola.count(counting))


def most_mentioned_by_all():
    with open(FILE_PATH, 'r') as f:
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

        # TODO: save it in a structure!! or not
        party_mentioned = {}
        for party in available_party_list:
            ola = doc_dict.get(party)
            for counting in available_party_list:
                if party == counting:
                    continue
                else:
                    counter = ola.count(counting)
                    val = party_mentioned.get(counting)
                    if val is None:
                        party_mentioned.update({counting: counter})
                    else:
                        party_mentioned.update({counting: counter + val})
        # print(party_mentioned)
        max_party = max(party_mentioned, key=party_mentioned.get)
        print(max_party + " is most mentioned in total of " + str(party_mentioned.get(max_party)) + " times")


def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    file = args['file']
    globally = args['globally']
    party = args['party']
    mention = args['mention']
    times = args['times']
    language = args['language']

    if language == "en":
        nlp = spacy.load('en_core_web_sm')
    elif language == "pt":
        nlp = spacy.load('pt')
    else:
        print("No language specified, using English package!")
    if file:
        print("Using file " + file)
    elif globally:
        get_most_named_entity_globally()
    elif party:
        get_most_named_entity_per_party()
    elif mention:
        most_mentioned_party_per_party()
    elif times:
        most_mentioned_by_all()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
