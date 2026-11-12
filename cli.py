from rag.service import request_chatbot


if __name__ == "__main__":
    print("Ask a question (empty or 'exit' to quit):")
    while True:
        input_query = input("you: ").strip()
        if not input_query or input_query.lower() in {"exit", "quit"}:
            break
        result = request_chatbot(input_query)
        print(f"chatbot: {result['chatbot']['message']}")
        print(f"record: {result}")
