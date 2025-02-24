import sys
import genanki
import re


def parse_file(filename):
    """Parses the input file and extracts questions and answers."""
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    qa_pairs = re.findall(r"Q:\s*(.*?)\nA:\s*(.*?)(?=\nQ:|\Z)", content, re.DOTALL)
    return qa_pairs


def create_anki_deck(deck_name, qa_pairs):
    """Creates an Anki deck from the extracted questions and answers."""
    model = genanki.Model(
        1607392319,
        "Simple Model",
        fields=[{"name": "Question"}, {"name": "Answer"}],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Question}}",
                "afmt": "{{FrontSide}}<hr id='answer'>{{Answer}}",
            }
        ],
    )

    deck = genanki.Deck(hash(deck_name), deck_name)

    for question, answer in qa_pairs:
        note = genanki.Note(model=model, fields=[question.strip(), answer.strip()])
        deck.add_note(note)

    return deck


def save_deck(deck, output_filename):
    """Saves the Anki deck as an .apkg file."""
    genanki.Package(deck).write_to_file(output_filename)
    print(f"Deck saved as {output_filename}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <deck_name>")
        sys.exit(1)

    input_file = sys.argv[1]
    deck_name = sys.argv[2]

    qa_pairs = parse_file(input_file)
    if not qa_pairs:
        print("No questions found in the file.")
        sys.exit(1)

    deck = create_anki_deck(deck_name, qa_pairs)
    save_deck(deck, f"{deck_name}.apkg")
