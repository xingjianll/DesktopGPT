import json
from json import JSONDecodeError


def store_pass(password: str):

    with open("pass.txt", "w") as f:
        f.write(password)


def get_pass() -> str:
    try:
        with open("pass.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        open("pass.txt", "w+")
        return ""


def store_conversations(conversations: dict[str, list]):
    with open("data.json", "w") as f:
        json.dump(conversations, f, indent=4)


def get_conversations() -> dict[str, list]:
    try:
        with open("data.json", "r") as f:
            try:
                data = json.load(f)
            except JSONDecodeError:
                data = None
            return data
    except FileNotFoundError:
        open("data.json", "w+")


def remember_me() -> bool:
    try:
        with open("config.txt", "r") as f:
            if f.read() == "Y":
                return True
            else:
                return False
    except FileNotFoundError:
        open("config.txt", "w+")
        return False
