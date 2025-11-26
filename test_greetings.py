from greetings import make_greeting, add_numbers

def test_make_greeting():
    assert make_greeting("Python") == "Hello, Python!"
    assert make_greeting("Developer") == "Hello, Developer!"

def test_add_numbers():
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0