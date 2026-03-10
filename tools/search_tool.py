from rag.retriever import retrieve_context

def search_docs(query: str, db):

    context = retrieve_context(db, query)

    return context