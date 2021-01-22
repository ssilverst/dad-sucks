from pathlib import Path

def get_highscore(filename):
    """Get the highscore (integer) from a text file."""
    file = Path(__file__).parent / filename
    try:
        high_score = int(file.read_text())
    except FileNotFoundError:
        high_score = 0
    except ValueError:
        raise ValueError(
            "File contents does not evaluate to string – highscore file corrupted."
        )
    return high_score


def save_highscore(filename, high_score):
    """Save an integer to a text file in the same directory as this file."""
    file = Path(__file__).parent / filename
    file.write_text(str(high_score))