from whoosh.index import create_in
from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import *
from whoosh import scoring
import csv
import sys
import re


def manifests(word):
    csv.field_size_limit(sys.maxsize)
    schema = Schema(linha=NUMERIC(stored=True), manifest_id=TEXT(stored=True), party=TEXT(stored=True), content=TEXT(stored=True))
    ix = create_in("dir", schema)
    with open("en_docs_clean.csv", 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        writer = ix.writer()
        i = 2
        dic = {}
        for row in csv_reader:
            writer.add_document(linha=i, manifest_id=row['manifesto_id'], party=row['party'], content=row['text'])
            p = row["party"]
            if p not in dic:
                dic[p] = 0
            i = i + 1
        writer.commit()
    s_words = word.split(",")
    ix = open_dir("dir")
    with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
        qu = QueryParser("content", ix.schema, group=OrGroup)
        i = 0
        while i < len(s_words):
            dic = dict.fromkeys(dic, 0)
            man = []
            q = qu.parse(s_words[i])
            results = searcher.search(q, limit=None)
            print("Number of manifestos.")
            print("Keyword:", s_words[i])
            for s, r in enumerate(results):
                manifesto = r["manifest_id"]
                party = r["party"]
                if manifesto not in man:
                    man.append(manifesto)
                    dic[party] += 1
            print(dic)
            print("Score:", results.score(s))
            print("\n")

            i = i + 1


def keyword(word):
    with open("en_docs_clean.csv", 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        d = {}
        for row in csv_reader:
            p = row["party"]
            if p not in d:
                d[p] = 0
    ix = open_dir("dir")
    s_words = word.split(",")
    with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
        qu = QueryParser("content", ix.schema, group=OrGroup)
        i = 0
        while i < len(s_words):
            d = dict.fromkeys(d, 0)
            q = qu.parse(s_words[i])
            results = searcher.search(q, limit=None)
            print("Number of Keywords.")
            print("Keyword:", s_words[i])
            for s, r in enumerate(results):
                raw = r["content"]
                par = r["party"]
                raw2 = re.split("\W+", raw)
                for word in raw2:
                    if word.lower() == s_words[i].lower():
                        d[par] += 1
            print("Score:", results.score(s))
            print(d)
            i = i + 1
            print("\n")


def statistics():
    word = sys.argv[1]
    manifests(word)
    keyword(word)


if __name__ == "__main__":
    statistics()
