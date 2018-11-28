import spacy, sys, csv
import argparse

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load('en_core_web_sm')
csv.field_size_limit(sys.maxsize)
party_list = []
text_list = []
text_per_party_list=[]
available_party_list = ['Labour Party', 'Conservative Party', 'Liberal Democrats', 'Scottish National Party',
                        'United Kingdom Independence Party', 'Green Party of England and Wales', 'We Ourselves',
                        'Social Democratic and Labour Party', 'Ulster Unionist Party', 'The Party of Wales',
                        'Democratic Unionist Party']
# for party in party_list:
#         if party not in available_party_list:
#                 available_party_list.append(party)
#         count = count + 1

party_dict={'Labour Party':[1] }

def get_parser():
        parser = argparse.ArgumentParser(description="""PRI statistical analysis tool""")
        parser.add_argument('-f', '--file', dest='file', help="""receive file from stdin [default: no]""",
                            action="store")
        return parser


def magic():

        with open("../pri_project_data/en_docs_clean.csv", 'r') as f:
                blocksize = 947778
#                text = f.read(blocksize)
                csv_reader = csv.DictReader(f)
                for row in csv_reader:
                        party_list.append(row['party'])
                        text_list.append(row['text'])
                print(party_list[0])
                count=0
                for party in party_list:
                        if party in available_party_list:
                                if party_dict.get(party) is not None:
                                        party_dict.update({party:party_dict.get(party).append(count)})
                        count = count + 1
                # count2 =0
                # for party2 in party_list:
                #         if party2 in available_party_list:
                #                 val = available_party_list[count2].get(party2)
                #                 val.append(count2)
                #                 available_party_list[count2].update({party2:val})
                #         count2=count2+1


                print(party_dict)


                # while text:
                #         doc = nlp(text)
                #         for entity in doc.ents:
                #                 print(entity.text, entity.label_)
                #         text = ""


def main():
        parser = get_parser()
        args = vars(parser.parse_args())
        file = args['file']

        if file:
                print("Using file " + file)
        else:
                magic()

if __name__=="__main__":
    main()

#doc = nlp(text)

# Find named entities, phrases and concepts
#for entity in doc.ents:
#    print(entity.text, entity.label_)
