"""Deterministic sentence spans for evidence quotes.

The enricher shows the model each review as a list of sentences and asks only for
the index of the evidence sentence. Code then expands that index back into
`text[start:end]`, so every evidence_quote is an exact substring of the source
text by construction (no copied or "fixed up" quotes from the model).
"""
from __future__ import annotations

import re

# A sentence ends after terminal punctuation (plus closing quotes/brackets and
# trailing emoji-free spaces) or at a line break.
_BOUNDARY = re.compile(r"[.!?…]+[\"')\]]*(?=\s)|\r\n|\r|\n")

MAX_SENTENCES = 40  # longer reviews: the tail is merged into the last span


def sentence_spans(text: str) -> list[tuple[int, int]]:
    """Return [(start, end)] spans with surrounding whitespace trimmed.

    Every span is nonempty and `text[start:end]` is an exact substring. A text
    with no boundary is one span. Blank text returns [].
    """
    spans: list[tuple[int, int]] = []
    pos = 0
    for m in _BOUNDARY.finditer(text):
        end = m.end() if m.group(0)[:1] not in "\r\n" else m.start()
        _add(text, pos, end, spans)
        pos = m.end()
    _add(text, pos, len(text), spans)
    if len(spans) > MAX_SENTENCES:
        spans = spans[: MAX_SENTENCES - 1] + [(spans[MAX_SENTENCES - 1][0], spans[-1][1])]
    return spans


def _add(text: str, start: int, end: int, spans: list) -> None:
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    if end > start:
        spans.append((start, end))


def sentences(text: str) -> list[str]:
    return [text[a:b] for a, b in sentence_spans(text)]
