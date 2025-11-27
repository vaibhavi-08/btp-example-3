from greetings import make_greeting, add_numbers


def main():
    user_name = "World"

    # Use the greeting function
    message = make_greeting(user_name)
    print(message)

    # Use the math function
    result = add_numbers(5, 7)
    print(f"5 + 7 = {result}")


if __name__ == "__main__":
    main()
