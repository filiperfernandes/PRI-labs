from whoosh.index import create_in
from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import *
import re


def index():
    index_list = []
    schema = Schema(id=NUMERIC(stored=True), content=TEXT)
    ix = create_in("dir", schema)
    fp = open("pri_cfc.txt", 'r')
    text = fp.read()
    words = re.split("\W+", text)
    for word in words:
        if word.isdigit() and len(word) == 5:
            index_list.append(word)

    writer = ix.writer()
    i = 0
    while i < len(index_list):
        writer.add_document(id=index_list[i], content='doc ' + str(i))
        i = i + 1
    writer.commit()


def unindex():
    ix = open_dir("dir")
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema, group=OrGroup).parse('doc')
        results = searcher.search(query, limit=1000000)
        for r in results:
            print(r)
    print("Number of results:", results.scored_length())


if __name__ == "__main__":
    index()
    unindex()
