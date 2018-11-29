from whoosh.index import create_in
from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import *
import csv
import sys
import re
import nltk

dict={}


def manifests(word):
    csv.field_size_limit(sys.maxsize)
    schema = Schema(linha=NUMERIC(stored=True), manifest_id=TEXT(stored=True), party=TEXT(stored=True), content=TEXT(stored=True))
    ix = create_in("dir", schema)
    with open("en_docs_clean.csv", 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        writer = ix.writer()
        i = 2
        for row in csv_reader:
            writer.add_document(linha=i, manifest_id=row['manifesto_id'], party=row['party'], content=row['text'])
            i = i + 1
        writer.commit()
    ix = open_dir("dir")
    with ix.searcher() as searcher:
        qu = QueryParser("content", ix.schema, group=OrGroup)
        q = qu.parse(word)
        results = searcher.search(q, sortedby="manifest_id", limit=None)
        m = ""
        p = ""
        nr_manifestos = 0
        for r in results:
            manifesto = r["manifest_id"]
            party = r["party"]
            if party != p and manifesto != m:
                if nr_manifestos != 0:
                    print(p, ":", nr_manifestos, "manifestos")
                nr_manifestos = 0
                p = party
                m = manifesto
                nr_manifestos = nr_manifestos + 1

            if party == p and manifesto != m:
                nr_manifestos = nr_manifestos + 1

            else:
                nr_manifestos = nr_manifestos
        print(p, ":", nr_manifestos, "manifestos")

        for res in results:
            print(res)


def keyword(word):
    csv.field_size_limit(sys.maxsize)
    schema = Schema(linha=NUMERIC(stored=True), manifest_id=TEXT(stored=True), party=TEXT(stored=True),
                    content=TEXT(stored=True))
    ix = create_in("dir", schema)
    with open("en_docs_clean.csv", 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        writer = ix.writer()
        i = 2
        for row in csv_reader:
            writer.add_document(linha=i, manifest_id=row['manifesto_id'], party=row['party'], content=row['text'])
            i = i + 1
        writer.commit()
    s_words = word.split(",")
    l = len(s_words)
    with ix.searcher() as searcher:
        qu = QueryParser("content", ix.schema, group=OrGroup)
        i = 0
        while i < len(s_words):
            q = qu.parse(s_words[i])
            results = searcher.search(q, sortedby="manifest_id", limit=None)
            print(s_words[i])
            listWords = []
            x = 0
            for r in results:
                raw = r["content"]
                par = r["party"]
                raw2 = re.split("\W+", raw)
                for word in raw2:
                    if word.lower() == s_words[i].lower():
                        dict[i] = par

            print(x)
            i = i + 1





def statistics():
    word = sys.argv[1]
    #manifests(word)
    keyword(word)


if __name__ == "__main__":
    statistics()
