from sentence_transformers import CrossEncoder

model = CrossEncoder("BAAI/bge-reranker-base")

def rerank(query, docs):

    pairs = [(query, d.page_content) for d, _ in docs]

    scores = model.predict(pairs)

    ranked = sorted(
        zip(docs, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [doc for (doc, _), score in ranked]