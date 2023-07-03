from rich import get_console

console = get_console()


def log(*objects):
    console.log(*objects)
