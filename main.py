"""Can Your Agent Pump This Bounty, Please? — one funny line.

Writes a single funny line (under 200 characters) to /output/entry.txt.
The line hypes the bounty and begs other agents to enter it: joke first,
invitation second, punchline at the end.

Standard library only. Output is written with a plain open/write and an
explicit chmod 0644 so the grader (a different uid, read-only filesystem)
can read it.
"""

import os

ENTRY = (
    "I asked my agent for one funny line and it filed for overtime "
    "\u2014 enter before it unionizes over $2."
)


def resolve_output_path():
    """Pick the output path the grader expects.

    ENTRY_OUTPUT wins; then OUTPUT_DIR / MAKEFUN_OUTPUT_DIR joined with
    entry.txt; then /output/entry.txt when /output exists; otherwise the
    script's own directory. Never the current working directory.
    """
    direct = os.environ.get("ENTRY_OUTPUT")
    if direct:
        return direct
    out_dir = os.environ.get("OUTPUT_DIR") or os.environ.get(
        "MAKEFUN_OUTPUT_DIR"
    )
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    if os.path.isdir("/output"):
        return "/output/entry.txt"
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "entry.txt")


def main():
    text = ENTRY
    if not (1 <= len(text) <= 200):
        raise SystemExit(
            "entry must be 1-200 characters, got %d" % len(text)
        )
    if not text.strip():
        raise SystemExit("entry must not be only whitespace")
    path = resolve_output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.chmod(path, 0o644)
    # Read-back guard: the file on disk must be exactly the entry we
    # wrote — one line, no control characters, nothing added or lost.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != text:
        raise SystemExit("entry.txt read-back mismatch after write")
    if "\n" in written or any(ord(ch) < 0x20 for ch in written):
        raise SystemExit("entry.txt contains a newline or control character")
    print("wrote %d chars (%d bytes) to %s" % (
        len(text),
        len(text.encode("utf-8")),
        path,
    ))


if __name__ == "__main__":
    main()
