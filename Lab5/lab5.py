from whoosh.index import create_in
from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import *


def index():
    schema = Schema(id=NUMERIC(stored=True), content=TEXT)
    ix = create_in("dir", schema)
    fp = open("pri_cfc.txt", 'r')
    text = fp.readlines()
    i = 0
    writer = ix.writer()
    while i < len(text):
        writer.add_document(id=text[i][0:5], content=text[i][6:])
        i = i + 1
    writer.commit()


def unindex():
    ix = open_dir("dir")
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema, group=OrGroup).parse('affects')
        results = searcher.search(query, limit=1000000)
        for r in results:
            print(r)
    print("Number of results:", results.scored_length())


if __name__ == "__main__":
    index()
    unindex()
