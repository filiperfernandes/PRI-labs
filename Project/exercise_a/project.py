from whoosh.index import create_in
from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import *
import csv
import sys


def index():
    csv.field_size_limit(sys.maxsize)
    schema = Schema(party=TEXT(stored=True), content=TEXT)
    ix = create_in("dir", schema)
    with open("en_docs_clean.csv", 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        writer = ix.writer()
        for row in csv_reader:
            writer.add_document(party=row['party'], content=row['text'])
        writer.commit()
    ix = open_dir("dir")
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema, group=OrGroup).parse('United')
        results = searcher.search(query, limit=10000000)
        for r in results:
            print(r)
    print(results.scored_length(), 'manifestos')


if __name__ == "__main__":
    index()
