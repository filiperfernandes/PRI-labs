from whoosh.index import create_in
from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import *


def index():
    list = {}
    schema = Schema(id=NUMERIC(stored=True), content=TEXT)
    ix = create_in("dir", schema)
    fp = open("pri_cfc.txt", 'r')
    text = fp.read()
    texto = text.split(" ")
    print(texto)
    writer = ix.writer()
    writer.add_document(id=1, content=text)
    writer.commit()


def unindex():
    ix = open_dir("dir")
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema, group=OrGroup).parse(u"first document")
        results = searcher.search(query, limit=100)
        for r in results:
            print(r)
    print("Number of results:", results.scored_length())


if __name__ == "__main__":
    index()
    #unindex()
