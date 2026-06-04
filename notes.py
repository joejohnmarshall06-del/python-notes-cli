import argparse
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("notes.json")


def load_notes():
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_notes(notes):
    DATA_FILE.write_text(json.dumps(notes, indent=2), encoding="utf-8")


def next_id(notes):
    return max((note["id"] for note in notes), default=0) + 1


def add_note(text):
    notes = load_notes()
    note = {"id": next_id(notes), "text": text, "done": False}
    notes.append(note)
    save_notes(notes)
    print(f"Added note #{note['id']}")


def list_notes():
    notes = load_notes()
    if not notes:
        print("No notes yet.")
        return

    for note in notes:
        status = "x" if note["done"] else " "
        print(f"[{status}] {note['id']}: {note['text']}")


def mark_done(note_id):
    notes = load_notes()
    for note in notes:
        if note["id"] == note_id:
            note["done"] = True
            save_notes(notes)
            print(f"Completed note #{note_id}")
            return
    print(f"Note #{note_id} was not found.")


def delete_note(note_id):
    notes = load_notes()
    remaining = [note for note in notes if note["id"] != note_id]
    if len(remaining) == len(notes):
        print(f"Note #{note_id} was not found.")
        return
    save_notes(remaining)
    print(f"Deleted note #{note_id}")


def main():
    parser = argparse.ArgumentParser(description="Manage local notes.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("text")

    subparsers.add_parser("list")

    done_parser = subparsers.add_parser("done")
    done_parser.add_argument("id", type=int)

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("id", type=int)

    args = parser.parse_args()

    if args.command == "add":
        add_note(args.text)
    elif args.command == "list":
        list_notes()
    elif args.command == "done":
        mark_done(args.id)
    elif args.command == "delete":
        delete_note(args.id)


if __name__ == "__main__":
    main()
