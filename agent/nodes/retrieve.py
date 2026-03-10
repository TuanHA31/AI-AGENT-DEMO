from rag.retriever import retrieve_context

def retrieve_node(state, db):
    question = state["question"]

    context = retrieve_context(db, question)

    state["context"] = context
    return state