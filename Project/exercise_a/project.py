from whoosh.index import create_in
from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import *
import csv
import sys


def index():
    csv.field_size_limit(sys.maxsize)
    schema = Schema(id=NUMERIC(stored=True), manifest_id=TEXT(stored=True), party=TEXT(stored=True), content=TEXT)
    ix = create_in("dir", schema)
    with open("en_docs_clean.csv", 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        writer = ix.writer()
        i = 0
        for row in csv_reader:
            i = i + 1
            writer.add_document(id=i, manifest_id=row['manifesto_id'], party=row['party'], content=row['text'])
        writer.commit()
    ix = open_dir("dir")
    with ix.searcher() as searcher:
        qu = QueryParser("content", ix.schema)
        q = qu.parse("United")
        results = searcher.search(q, sortedby="manifest_id", limit=None)
        for r in results:
            print(r)
    print(results.scored_length(), 'manifestos')
    return results


def statistics():
    results = index()


if __name__ == "__main__":
    statistics()
