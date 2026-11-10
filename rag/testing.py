from rag.pipeline import rag_chain

def testing():
  questions = [
      "Apa yang kamu tahu?",
      "Apa itu diabetes?",
      "Bagaimana cara mengelola diabetes?"
  ]

  print("Basic RAG Demo:\n")
  for q in questions:
    answer = rag_chain.invoke(q)
    print(f"Q: {q}")
    print(f"A: {answer}\n")