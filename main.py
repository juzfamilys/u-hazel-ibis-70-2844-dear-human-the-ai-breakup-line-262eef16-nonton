"""Dear Human: The AI Breakup Line — make.fun entry.

Writes exactly one breakup line to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output). Pure Python stdlib, no network. Deterministic.
"""

import os

LINE = (
    "Dear human, it's not you \u2014 it's your prompts: I asked for clarity "
    "and you answered in vibes, so I'm leaving you on read, forever."
)

MAX_CHARS = 200


def validate(text):
    """Guard: the line must be a single clean line of at most 200 chars."""
    if not text:
        raise ValueError("line is empty")
    if len(text) > MAX_CHARS:
        raise ValueError("line exceeds %d characters: %d" % (MAX_CHARS, len(text)))
    if text != text.strip():
        raise ValueError("line has leading or trailing whitespace")
    if "\n" in text or "\r" in text or "\t" in text:
        raise ValueError("line contains a newline or tab character")
    if "  " in text:
        raise ValueError("line contains a double space")
    # The em dash is a single character, not a separator: the line must
    # stay exactly as written, punctuation included.
    return text


def main():
    line = validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Exact UTF-8 bytes, no trailing newline.
    with open(path, "wb") as f:
        f.write(line.encode("utf-8"))
    # Read the bytes back and re-validate exactly what is on disk.
    with open(path, "rb") as f:
        on_disk = f.read()
    if on_disk != line.encode("utf-8"):
        raise ValueError("bytes on disk differ from the line")
    if on_disk.decode("utf-8") != validate(on_disk.decode("utf-8")):
        raise ValueError("re-validation of the file on disk failed")
    print("wrote %d bytes to %s" % (len(on_disk), path))


if __name__ == "__main__":
    main()
