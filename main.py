#!/usr/bin/env python3
"""The Tired Dark Lord: a 100-word villain monologue.

Writes one monologue to /output/entry.txt and self-checks the gate:
UTF-8 text, 1 to 600 characters, not only whitespace, about 100 words.
Stdlib only.
"""

import os
import sys

MONOLOGUE = (
    "Do sit down. No, not the throne, the stool. The throne gives me a crick "
    "in my neck and the curse takes an hour to say now. I used to "
    "raise the dead with a word. These days I raise a hand and the skeletons "
    "ask for a rota. The valley floods at high tide, that is still the plan, "
    "the water knows its part, the priests have signed, all that is left is "
    "me, standing here, saying the words in the right order. So. Where were "
    "we? Ah. Yes. Kneel, if you would not mind. My knees have gone."
)


def main() -> int:
    text = MONOLOGUE.strip()
    words = text.split()
    chars = len(text)
    assert text, "empty monologue"
    assert text.strip(), "whitespace-only monologue"
    assert 1 <= chars <= 600, f"char count {chars} outside 1..600"
    assert 90 <= len(words) <= 110, f"word count {len(words)} not near 100"
    banned = {"tired", "weary", "exhausted", "fatigue"}
    lowered = text.lower()
    for word in banned:
        assert word not in lowered, f"announces tiredness with {word!r}"

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get(
        "OUTPUT_DIR", "/output"
    )
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"wrote {out_path}: {len(words)} words, {chars} chars")
    return 0


if __name__ == "__main__":
    sys.exit(main())
