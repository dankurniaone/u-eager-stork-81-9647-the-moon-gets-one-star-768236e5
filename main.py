#!/usr/bin/env python3
"""The Moon Gets One Star — writes the winning one-star review to /output/entry.txt.

Gate: UTF-8 text, 1 to 120 characters, not only whitespace.
Judge: a one-star review of the Moon itself, funniest wins pairwise.
The flooded moves are craters, cheese and brightness, so the entry dodges
all three and lands on a grievance only the Moon could earn: it makes no
light of its own, it reflects the Sun's, and it takes all the credit.
A line that would work for any product with the Moon swapped out is weaker
than one that could only be about the Moon, and this one is Moon-only:
no other product steals the Sun's light and takes the credit for it.

Winner (98 chars, tournament 5/5/5 = 15):
    One star. It doesn't even make its own light, it just reflects the Sun's
    and takes all the credit.
"""

import argparse
import sys
from pathlib import Path

ENTRY = "One star. It doesn't even make its own light, it just reflects the Sun's and takes all the credit."

TOURNAMENT = [
    # (line, specificity, surprise, freshness)
    ("One star. It doesn't even make its own light, it just reflects the Sun's and takes all the credit.", 5, 5, 5),
    ("One star. After 4.5 billion years it still only shows me one side. Rude, secretive, no effort.", 5, 4, 5),
    ("One star. Flooded my garden twice a month and blamed the tide. Zero accountability.", 4, 4, 4),
    ("One star. Ordered a full moon, arrived half. False advertising, and it does this every month.", 5, 5, 4),
    ("One star. No atmosphere, no wifi, and it still expects me to look up at it every night.", 4, 4, 4),
    ("One star. Works nights only, vanishes for a week every month, and the overtime is eclipses.", 4, 4, 3),
    ("One star. It controls the tides and still let my basement flood. Management refused to comment.", 4, 4, 4),
]


def check_entry(text: str) -> dict:
    """Validate the entry against the sealed scorer's gate."""
    chars = len(text)
    return {
        "chars": chars,
        "bytes": len(text.encode("utf-8")),
        "valid": 1 <= chars <= 120 and text.strip() != "",
        "words": len(text.split()),
        "sentences": text.count(".") + text.count("!") + text.count("?"),
    }


def write_entry(out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(ENTRY, encoding="utf-8")
    return target


def self_test() -> bool:
    """Write twice and confirm byte-identical output."""
    first = Path("/tmp/moon-self-test-a/entry.txt")
    second = Path("/tmp/moon-self-test-b/entry.txt")
    write_entry(first.parent)
    write_entry(second.parent)
    return first.read_bytes() == second.read_bytes()


def print_tournament() -> None:
    print("candidate tournament (specificity / surprise / freshness):")
    for i, (line, spec, surp, fresh) in enumerate(TOURNAMENT, 1):
        total = spec + surp + fresh
        mark = " <-- WINNER" if line == ENTRY else ""
        print(f"  {i}. {spec}/{surp}/{fresh} = {total:2d}  {line}{mark}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Write the Moon one-star review.")
    parser.add_argument("--out", default="/output", help="output directory")
    parser.add_argument("--check", action="store_true", help="validate the entry and exit")
    parser.add_argument("--self-test", action="store_true", help="check byte-identical output")
    parser.add_argument("--tournament", action="store_true", help="print the candidate tournament")
    args = parser.parse_args(argv)

    if args.tournament:
        print_tournament()
        return 0

    if args.check:
        result = check_entry(ENTRY)
        print(f"chars={result['chars']} bytes={result['bytes']} words={result['words']} sentences={result['sentences']} valid={result['valid']}")
        return 0 if result["valid"] else 1

    if args.self_test:
        ok = self_test()
        print(f"self-test byte-identical: {ok}")
        return 0 if ok else 1

    target = write_entry(Path(args.out))
    result = check_entry(ENTRY)
    print(f"wrote {target} ({result['chars']} chars, valid={result['valid']})")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
