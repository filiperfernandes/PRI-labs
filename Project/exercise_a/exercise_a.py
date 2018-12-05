from whoosh.index import create_in
from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import *
from whoosh import scoring
import csv
import sys
import re


def index():
    csv.field_size_limit(sys.maxsize)
    schema = Schema(linha=NUMERIC(stored=True), manifest_id=TEXT(stored=True), party=TEXT(stored=True),
                    content=TEXT(stored=True))
    ix = create_in("dir", schema)
    with open("pt_docs_clean.csv", 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        writer = ix.writer()
        i = 2
        dic = {}
        d = {}
        for row in csv_reader:
            writer.add_document(linha=i, manifest_id=row['manifesto_id'], party=row['party'], content=row['text'])
            i = i + 1
            p = row["party"]
            if p not in dic:
                dic[p] = 0
            if p not in d:
                d[p] = 0
        writer.commit()
    return dic, d


def manifests_keywords(word, dic, d):
    s_words = word.split(",")
    ix = open_dir("dir")
    with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
        qu = QueryParser("content", ix.schema, group=OrGroup)
        i = 0
        while i < len(s_words):
            dic = dict.fromkeys(dic, 0)
            d = dict.fromkeys(d, 0)
            man = []
            q = qu.parse(s_words[i])
            results = searcher.search(q, limit=None)
            for s, r in enumerate(results):
                manifesto = r["manifest_id"]
                party = r["party"]
                if manifesto not in man:
                    man.append(manifesto)
                    dic[party] += 1
                content = r["content"]
                split_words = re.split("\W+", content)
                for word in split_words:
                    if word.lower() == s_words[i].lower():
                        d[party] += 1
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


def main():
    word = sys.argv[1]
    dic, d = index()
    manifests_keywords(word, dic, d)


if __name__ == "__main__":
    main()
