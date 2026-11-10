from rag.pipeline import rag_chain

def testing():
  questions = [
      "What is Langchain?",
      "Who created Langchain?",
      "what is LangGraph used for?",
      "Who is Satoshi Nakamoto?"
  ]

  print("Basic RAG Demo:\n")
  for q in questions:
    answer = rag_chain.invoke(q)
    print(f"Q: {q}")
    print(f"A: {answer}\n")
    
def testing2():
  questions2 = [
      "who is new president of USA?",
      "who are you?"
  ]

  print("Basic RAG Demo2:\n")
  for q in questions2:
    answer = rag_chain.invoke(q)
    print(f"Q: {q}")
    print(f"A: {answer}\n")