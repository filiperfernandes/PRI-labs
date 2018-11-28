from whoosh.index import create_in
from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import *
import csv
import sys


def index(word):
    print(word)
    csv.field_size_limit(sys.maxsize)
    schema = Schema(manifest_id=TEXT(stored=True), party=TEXT(stored=True), content=TEXT)
    ix = create_in("dir", schema)
    with open("en_docs_clean.csv", 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        writer = ix.writer()
        for row in csv_reader:
            writer.add_document(manifest_id=row['manifesto_id'], party=row['party'], content=row['text'])
        writer.commit()
    ix = open_dir("dir")
    with ix.searcher() as searcher:
        qu = QueryParser("content", ix.schema, group=OrGroup)
        q = qu.parse(word)
        results = searcher.search(q, sortedby="manifest_id", limit=None)
        #l_id = []
        m = ""
        p = ""
        nr_manifestos = 0
        for r in results:
            manifesto = r["manifest_id"]
            party = r["party"]
            if party != p and manifesto != m:
                if nr_manifestos != 0:
                    print(p,":", nr_manifestos, "manifestos")
                nr_manifestos = 0
                p = party
                m = manifesto
                nr_manifestos = nr_manifestos + 1

            if party == p and manifesto != m:
                nr_manifestos = nr_manifestos + 1

            else:
                nr_manifestos = nr_manifestos
        print(p, ":", nr_manifestos, "manifestos")






        #list_manifest = remove(l_id)
        #print("\n", len(list_manifest), "manifests")
        #print(results.scored_length(), "manifests in total")
        #return results


def statistics():
    word = sys.argv[1]
    results = index(word)


def remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list


if __name__ == "__main__":
    statistics()
