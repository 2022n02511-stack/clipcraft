
import argparse
import subprocess
import sys

from core.dbus_server import process_text
from storage.history import save


def read_clipboard():
    try:
        result = subprocess.run(
            ["wl-paste", "--no-newline"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5
        )

        if result.returncode != 0:
            raise RuntimeError("Could not read clipboard.")

        return result.stdout

    except FileNotFoundError:
        raise RuntimeError("wl-paste is not installed.")

    except subprocess.TimeoutExpired:
        raise RuntimeError("Clipboard read timed out.")


def write_clipboard(text):
    try:
        result = subprocess.run(
            ["wl-copy"],
            input=text,
            text=True,
            encoding="utf-8",
            capture_output=True,
            timeout=5
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "Could not update clipboard.")

    except FileNotFoundError:
        raise RuntimeError("wl-copy is not installed.")

    except subprocess.TimeoutExpired:
        raise RuntimeError("Clipboard write timed out.")


def main():
    parser = argparse.ArgumentParser(
        prog="clipcraft",
        description="Format clipboard text manually."
    )

    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read text from standard input instead of clipboard."
    )

    args = parser.parse_args()

    try:
        original = sys.stdin.read() if args.stdin else read_clipboard()

        if not original.strip():
            print("[ClipCraft] No text to format.")
            return 1

        print("[ClipCraft] Formatting...")

        formatted = process_text(original)

        if not formatted:
            print("[ClipCraft] Formatting returned empty text. Clipboard unchanged.")
            return 1

        if formatted != original and not args.stdin:
            write_clipboard(formatted)

        save(original, formatted)

        if args.stdin:
            sys.stdout.write(formatted)
        else:
            print("[ClipCraft] Clipboard updated successfully.")

        return 0

    except Exception as error:
        print(f"[ClipCraft] Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
