from rag.config import RETRIEVE_K
from rag.pipeline import rag_chain, vector_store

def testing():
  questions = [
      "Apa yang kamu tahu?",
      "Apa itu diabetes?",
      "Bagaimana cara mengelola diabetes?"
  ]

  print("Basic RAG Demo:\n")
  for q in questions:
    retrieved = vector_store.similarity_search_with_score(q, k=RETRIEVE_K)
    print(f"Q: {q}")
    print("Retrieved:")
    for doc, score in retrieved:
      source = doc.metadata.get("source", "?").split("/")[-1]
      page = doc.metadata.get("page", "?")
      snippet = doc.page_content[:120].replace("\n", " ")
      print(f"  [dist={score:.4f}] {source} p{page}: {snippet}...")
    answer = rag_chain.invoke(q)
    print(f"A: {answer}\n")
