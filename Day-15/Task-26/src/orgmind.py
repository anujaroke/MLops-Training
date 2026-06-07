from dotenv import load_dotenv

from rag_core import RagEngine

BANNER = r"""
  ____            __  ___          __
 / __ \________  /  |/  /___ _____/ /__
/ / / / ___/ _ \/ /|_/ / __ `/ __  / _ \
/ /_/ / /  /  __/ /  / / /_/ / /_/ /  __/
\____/_/   \___/_/  /_/\__,_/\__,_/\___/
"""


def main():
    load_dotenv()

    print(BANNER)
    print("Loading OrgMind...\n")

    engine = RagEngine()
    try:
        engine.build()
    except Exception as exc:
        print(str(exc))
        return

    print("Vector database ready!")
    print("🤖OrgMind is awake. Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in {"exit", "quit", "bye"}:
            print("Goodbye!")
            break
        if not question:
            continue

        response, sources = engine.answer(question)

        print(f"OrgMind: {response}\n")
        if sources:
            print("Sources: " + ", ".join(sources) + "\n")


if __name__ == "__main__":
    main()
