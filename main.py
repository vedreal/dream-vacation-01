#!/usr/bin/env python3
"""One Emoji, One Dream Vacation — make.fun entry.

The bounty asks for exactly one emoji, nothing else, standing in for
the trip of your dreams. A judge model (a travel editor collecting
wordless postcards) reads entries two at a time and picks the one that
most makes a stranger want to book the flight.

The judge weighs, most important first:
  1. Exactly one emoji, no words, landing on a dream vacation
     (a beach, a mountain, a plane, a hammock, a faraway place).
  2. Evokes the trip vividly at a glance, like a postcard.
  3. Feels personal and specific rather than generic.
  4. Carries a spark of wit or surprise.
  5. Reads instantly across cultures and screens, clear at small size.

This program scores ten fresh candidate emojis against those five
criteria (weights 5/4/3/2/1, each criterion 0-5, max 75), picks the
highest scorer (shortest wins a tie), and writes it to
/output/entry.txt. The gate requires 1-8 UTF-8 characters, so the
winner must be a single code point with no variation selector.
"""

# (emoji, rationale, scores per criterion in the judge's order)
CANDIDATES = [
    ("\U0001f3dd\ufe0f", "Desert island: the ultimate postcard, but the "
     "first emoji every entrant reaches for.", [5, 4, 1, 1, 5]),
    ("\U0001f3d6\ufe0f", "Beach with umbrella: the canonical holiday, "
     "so canonical it says nothing personal.", [5, 4, 1, 1, 5]),
    ("\U0001f305", "Sunrise over the sea: gorgeous and vivid, but a "
     "sunrise belongs to every coast on earth.", [5, 5, 2, 2, 5]),
    ("\U0001f5fb", "Mount Fuji: one mountain, one place, the most "
     "recognisable postcard on the planet; a mountain is named in the "
     "brief itself, and the snow cap reads at any size.", [5, 5, 5, 2, 5]),
    ("\U0001f30c", "Milky Way: a night under a dark sky in the desert "
     "or the high mountains; specific, wondrous, surprising.", [4, 5, 5, 4, 4]),
    ("\U0001f3d4\ufe0f", "Snow-capped mountain: majestic and readable, "
     "but any range could be any range.", [5, 4, 3, 2, 5]),
    ("\u26f5", "Sailboat: the Aegean, the trade winds, a week with "
     "nowhere to be; specific and calm.", [5, 4, 4, 2, 5]),
    ("\U0001f30b", "Volcano: lava fields in Iceland or Hawaii, a trip "
     "with real adventure in it; surprising, but not everyone's dream.",
     [4, 4, 5, 4, 5]),
    ("\U0001f41a", "Shell: the souvenir of the beach, personal and "
     "quiet; too small a picture to make a stranger book a flight.",
     [3, 3, 5, 4, 5]),
    ("\U0001f6f6", "Canoe: a still lake at dawn, paddling nowhere in "
     "particular; serene and specific, but low on postcard punch.",
     [4, 4, 4, 3, 5]),
]

WEIGHTS = [5, 4, 3, 2, 1]


def score(entry):
    """Weighted score out of 75, following the judge's criteria order."""
    _, _, scores = entry
    return sum(w * s for w, s in zip(WEIGHTS, scores))


def rank(candidates):
    """Highest score first; fewest bytes wins a tie (the site breaks
    exact ties on Judge win rate by smaller text, then earlier receipt)."""
    return sorted(
        candidates,
        key=lambda e: (-score(e), len(e[0].encode("utf-8"))),
    )


def main():
    ranked = rank(CANDIDATES)
    winner, rationale, scores = ranked[0]
    runner_up = ranked[1][0]

    # Gate: /output/entry.txt must be UTF-8 text of 1 to 8 characters,
    # not only white space, and exactly one emoji, nothing else.
    text = winner
    assert 1 <= len(text) <= 8, "entry must be 1-8 characters"
    assert text.strip(), "entry must not be only white space"
    assert len(text) == 1, "entry must be exactly one emoji"

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"winner: {winner}  (score {score(ranked[0])}/75)")
    print(f"  {rationale}")
    print(f"runner-up: {runner_up}  (score {score(ranked[1])}/75)")
    print(f"wrote {path}: {len(text.encode('utf-8'))} bytes, "
          f"{len(text)} character")


if __name__ == "__main__":
    import os

    main()
