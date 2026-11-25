#!/usr/bin/env python3
"""The Tired Dark Lord: a 100-word villain monologue.

This runner writes the monologue to entry.txt inside the harness output
directory and checks it against the competition gate before writing:
the text must be UTF-8, non-empty, between 1 and 600 characters, and
close to 100 words. It also refuses to state the tiredness outright —
the weariness has to live in the pauses and the paperwork, not in a
word like "tired".

Stdlib only: no third-party imports, so the grader's bare python3 can
run this as-is.
"""

import os
import re
import sys

# The entry itself. Do not edit a single word: the count and the
# character total below were measured against exactly this text.
MONOLOGUE = (
    "Do sit down. No, not the throne, the stool. The throne gives me a crick "
    "in my neck and the curse takes an hour to say now. I used to "
    "raise the dead with a word. These days I raise a hand and the skeletons "
    "ask for a rota. The valley floods at high tide, that is still the plan, "
    "the water knows its part, the priests have signed, all that is left is "
    "me, standing here, saying the words in the right order. So. Where were "
    "we? Ah. Yes. Kneel, if you would not mind. My knees have gone."
)

TARGET_WORDS = 100
WORD_TOLERANCE = 10
MAX_CHARS = 600

# Words that would say the tiredness out loud instead of showing it.
# The monologue must earn the mood through the rota, the crick in the
# neck, the hour-long curse — never through one of these.
FORBIDDEN_WORDS = ("tired", "weary", "exhausted", "fatigue")


def word_count(text):
    """How many whitespace-separated words the text holds."""
    return len(text.split())


def char_count(text):
    """How many characters the text holds, spaces included."""
    return len(text)


def find_forbidden_words(text):
    """Any forbidden word present as a whole word, in order.

    Word boundaries matter: a substring match would flag innocent
    words that merely contain a forbidden one, so each word is
    matched on its own.
    """
    words = set(re.findall(r"[a-z]+", text.lower()))
    return [word for word in FORBIDDEN_WORDS if word in words]


def validate_monologue(text):
    """Collect every gate violation; an empty list means the text passes.

    Each problem is a short human-readable string, so the runner can
    print all of them at once instead of dying on the first one.
    """
    problems = []
    if not text:
        problems.append("monologue is empty")
    if not text.strip():
        problems.append("monologue is whitespace only")
    chars = char_count(text)
    if not 1 <= chars <= MAX_CHARS:
        problems.append(f"{chars} chars is outside the 1..{MAX_CHARS} gate")
    words = word_count(text)
    low = TARGET_WORDS - WORD_TOLERANCE
    high = TARGET_WORDS + WORD_TOLERANCE
    if not low <= words <= high:
        problems.append(
            f"{words} words is outside the {low}..{high} band "
            f"around {TARGET_WORDS}"
        )
    for word in find_forbidden_words(text):
        problems.append(f"monologue states its tiredness with {word!r}")
    return problems


def resolve_output_dir():
    """Pick where entry.txt goes.

    The grading harness sets MAKEFUN_OUTPUT_DIR, so that wins. A plain
    OUTPUT_DIR is accepted as a fallback for local runs, and /output is
    the last resort when neither is set.
    """
    return (
        os.environ.get("MAKEFUN_OUTPUT_DIR")
        or os.environ.get("OUTPUT_DIR")
        or "/output"
    )


def write_entry(text, out_dir):
    """Write the monologue to entry.txt inside out_dir, creating it."""
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write(text)
    return out_path


def self_check(text):
    """Run the gate and report the result; True when it passes."""
    problems = validate_monologue(text)
    if problems:
        for problem in problems:
            print(f"self-check failed: {problem}", file=sys.stderr)
        return False
    print(
        f"self-check passed: {word_count(text)} words, "
        f"{char_count(text)} chars"
    )
    return True


def main(argv=None):
    """Validate the monologue, then write it.

    With --check, only run the self-check and write nothing, so the
    gate can be exercised without touching the output directory.
    """
    args = list(sys.argv[1:] if argv is None else argv)
    check_only = "--check" in args
    text = MONOLOGUE.strip()
    if not self_check(text):
        return 1
    if check_only:
        print("check only: nothing written")
        return 0
    out_path = write_entry(text, resolve_output_dir())
    print(
        f"wrote {out_path}: {word_count(text)} words, "
        f"{char_count(text)} chars"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
