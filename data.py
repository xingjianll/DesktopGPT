import json
from json import JSONDecodeError


def store_pass(password: str):
    with open("pass.txt", "w") as f:
        f.write(password)


def get_pass() -> str:
    with open("pass.txt", "r") as f:
        return f.read()


def store_conversations(conversations: dict[str, list]):
    with open("data.json", "w") as f:
        json.dump(conversations, f, indent=4)


def get_conversations() -> dict[str, list]:
    with open("data.json", "r") as f:
        try:
            data = json.load(f)
        except JSONDecodeError:
            data = None
        return data


def remember_me() -> bool:
    with open("config.txt", "r") as f:
        if f.read() == "Y":
            return True
        else:
            return False
