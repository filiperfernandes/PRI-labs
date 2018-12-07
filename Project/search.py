from whoosh.index import create_in
from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import *
from whoosh import scoring
import csv
import sys
import re
import argparse

FILE_PATH = "pri_project_data/en_docs_clean.csv"


def get_parser():
    parser = argparse.ArgumentParser(description="""PRI search tool""")
    parser.add_argument('-f', '--file', dest='file', help="""receive file from stdin [default: no]""",
                        action="store")
    parser.add_argument('-l', '--language', dest='language', help="""Specify language 'en' or 'pt'""",
                        action="store")
    parser.add_argument('-t', '--TF', help="""TF_IDF""",
                        action="store_true")
    parser.add_argument('-b', '--BM', help="""BM-25F""",
                        action="store_true")
    parser.add_argument('-fr', '--FR', help="""Frequency""",
                        action="store_true")
    parser.add_argument('-i', '--input', dest='input_args', help="""Words to search separated by commas 
    (word1,word2,word3)""",
                        action="store", required=True)
    return parser


def index():
    csv.field_size_limit(sys.maxsize)
    schema = Schema(linha=NUMERIC(stored=True), manifest_id=TEXT(stored=True), party=TEXT(stored=True),
                    content=TEXT(stored=True))
    ix = create_in("dir", schema)
    with open(FILE_PATH, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        writer = ix.writer()
        i = 2
        dic = {}
        d = {}
        di = {}
        for row in csv_reader:
            writer.add_document(linha=i, manifest_id=row['manifesto_id'], party=row['party'], content=row['text'])
            i = i + 1
            p = row["party"]
            if p not in dic:
                dic[p] = 0
            if p not in d:
                d[p] = 0
            if p not in di:
                di[p] = 0
        writer.commit()
    return dic, d, di


def manifests_keywords(word, dic, d, di, wheight):
    s_words = word.split(",")
    ix = open_dir("dir")
    with ix.searcher(weighting=wheight) as searcher:
        qu = QueryParser("content", ix.schema, group=OrGroup)
        i = 0
        lis = []
        while i < len(s_words):
            dic = dict.fromkeys(dic, 0)
            d = dict.fromkeys(d, 0)
            man = []
            q = qu.parse(s_words[i])
            results = searcher.search(q, limit=None)
            for s, r in enumerate(results):
                manifesto = r["manifest_id"]
                party = r["party"]
                if manifesto not in lis:
                    lis.append(manifesto)
                if manifesto not in man:
                    man.append(manifesto)
                    dic[party] += 1
                    di[party] += 1
                content = r["content"]
                split_words = re.split("\W+", content)
                for word in split_words:
                    if word.lower() == s_words[i].lower():
                        d[party] += 1
            print("List of manifestos of keyword:", s_words[i])
            print(man, "\n")
            print("Number of manifestos.")
            print("Keyword:", s_words[i], '\n')
            print(dic)
            print("\n")
            print("Number of Keywords.")
            print("Keyword:", s_words[i])
            print(d)
            print("\n")
            i = i + 1
        print("Manifestos of all keywords")
        print(lis, "\n")
        print("Total number of manifestos of all keywords")
        print(di)


def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    file = args['file']
    tf = args['TF']
    bm = args['BM']
    fr = args['FR']
    input_args = args['input_args']

    word = input_args
    dic, d, di = index()

    if file:
        print("Using file " + file)
        FILE_PATH = "pri_project_data/"+file

    if tf:
        manifests_keywords(word, dic, d, di, scoring.TF_IDF)
    elif bm:
        manifests_keywords(word, dic, d, di, scoring.BM25F)
    elif fr:
        manifests_keywords(word, dic, d, di, scoring.Frequency)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
