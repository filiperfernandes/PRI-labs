from whoosh.index import open_dir
from whoosh.qparser import *
ix = open_dir("indexdir")
with ix.searcher()
    query = QueryParser("content", ix.schema, group=OrGroup).parse(u"a query")
    results = searcher.search(query, limit=100)
    for i, r in enumerate(results):
        print(r, results.score(i))
