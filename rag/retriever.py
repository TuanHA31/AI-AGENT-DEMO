def retrieve_context(db, query, k=5):
    docs = db.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in docs])