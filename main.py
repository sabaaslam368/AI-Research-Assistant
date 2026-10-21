from agent import run_agent


def main():

    print()
    print("=" * 60)
    print("              AI RESEARCH ASSISTANT")
    print("=" * 60)

    print(
        "\nI can help you with:"
    )

    print(
        "  • Research questions"
    )

    print(
        "  • Local research files"
    )

    print(
        "  • Mathematical calculations"
    )

    print(
        "\nType 'exit' to close the application."
    )

    while True:

        print()

        user_question = input(
            "You: "
        ).strip()

        # Exit
        if user_question.lower() == "exit":

            print(
                "\nGoodbye!"
            )

            break

        # Empty input
        if not user_question:

            print(
                "Please enter a question."
            )

            continue

        print(
            "\nResearch Assistant:"
        )

        answer = run_agent(
            user_question
        )

        print(answer)


if __name__ == "__main__":

    main()