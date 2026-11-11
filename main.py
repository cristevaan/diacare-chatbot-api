from datetime import datetime

from rag.service import answer


def request_chatbot(query):
    user_record = {
        "sender": "user",
        "message": query,
        "timestamp": datetime.now().isoformat(),
    }
    answer_text = answer(query)
    chatbot_record = {
        "sender": "chatbot",
        "message": answer_text,
        "timestamp": datetime.now().isoformat(),
    }
    return {"user": user_record, "chatbot": chatbot_record}


if __name__ == "__main__":
    print("Ask a question (empty or 'exit' to quit):")
    while True:
        input_query = input("you: ").strip()
        if not input_query or input_query.lower() in {"exit", "quit"}:
            break
        result = request_chatbot(input_query)
        print(f"chatbot: {result['chatbot']['message']}")
        print(f"record: {result}")
