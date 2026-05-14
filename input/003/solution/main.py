"""Simple persistent to-do list with a CLI menu."""

import json
import os.path

DATA_FILE = "todos.json"


def load_todos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_todos(todos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


def next_id(todos):
    return max((t["id"] for t in todos), default=0) + 1


def show_todos(todos):
    if not todos:
        print("Nimekiri on tühi.")
        return
    for t in todos:
        marker = "[x]" if t["done"] else "[ ]"
        print(f"{t['id']}. {marker} {t['text']}")


def add_todo(todos, text):
    todos.append({"id": next_id(todos), "text": text, "done": False})
    save_todos(todos)


def mark_done(todos, todo_id):
    for t in todos:
        if t["id"] == todo_id:
            t["done"] = True
            save_todos(todos)
            return True
    return False


def delete_todo(todos, todo_id):
    for i, t in enumerate(todos):
        if t["id"] == todo_id:
            todos.pop(i)
            save_todos(todos)
            return True
    return False


def ask_int(prompt):
    raw = input(prompt).strip()
    try:
        return int(raw)
    except ValueError:
        return None


def main():
    todos = load_todos()

    while True:
        print("\n--- To-Do nimekiri ---")
        print("1) Vaata ülesandeid")
        print("2) Lisa uus")
        print("3) Märgi tehtuks")
        print("4) Kustuta")
        print("0) Välju")

        choice = input("Valik: ").strip()

        if choice == "1":
            show_todos(todos)
        elif choice == "2":
            text = input("Ülesande tekst: ").strip()
            if text:
                add_todo(todos, text)
                print("Lisatud.")
            else:
                print("Tekst ei tohi olla tühi.")
        elif choice == "3":
            show_todos(todos)
            todo_id = ask_int("Mis ID? ")
            if todo_id is not None and mark_done(todos, todo_id):
                print("Märgitud tehtuks.")
            else:
                print("Sellise ID-ga ülesannet ei leitud.")
        elif choice == "4":
            show_todos(todos)
            todo_id = ask_int("Mis ID? ")
            if todo_id is not None and delete_todo(todos, todo_id):
                print("Kustutatud.")
            else:
                print("Sellise ID-ga ülesannet ei leitud.")
        elif choice == "0":
            print("Nägemist!")
            break
        else:
            print("Kehtetu valik, palun proovi uuesti.")


if __name__ == "__main__":
    main()
