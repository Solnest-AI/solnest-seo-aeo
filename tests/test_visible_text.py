"""
Regression tests for accessible text extraction in parse_html.

These cover the failure modes found auditing a live animated marketing site,
where naive extraction returned "Watch what happensWWWWaaaattttcccchhhh..."
for an <h1> whose real text is "Watch what happens when AI meets your business."
"""

import os
import sys

import pytest

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SCRIPTS = os.path.join(_REPO_ROOT, "scripts")
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)

pytest.importorskip("bs4")
from bs4 import BeautifulSoup  # noqa: E402

from parse_html import _visible_text, parse_html  # noqa: E402


def _el(html, tag="h1"):
    return BeautifulSoup(html, "html.parser").find(tag)


def test_aria_hidden_character_duplicates_are_skipped():
    """Shutter/scramble animations duplicate each glyph in aria-hidden spans."""
    html = (
        '<h1><span class="sr-only">Watch what happens</span>'
        '<span aria-hidden="true">'
        '<span class="shutter-char">W</span><span class="shutter-slice">W</span>'
        '<span class="shutter-char">a</span><span class="shutter-slice">a</span>'
        "</span></h1>"
    )
    assert _visible_text(_el(html)) == "Watch what happens"


def test_nested_aria_hidden_is_skipped_at_any_depth():
    html = (
        "<h1>Real"
        '<div><section><span aria-hidden="true">JUNK</span></section></div>'
        "</h1>"
    )
    assert "JUNK" not in _visible_text(_el(html))


def test_aria_hidden_false_is_not_skipped():
    html = '<h1>Keep <span aria-hidden="false">this</span></h1>'
    assert _visible_text(_el(html)) == "Keep this"


def test_whitespace_between_inline_nodes_survives():
    """get_text(strip=True) deletes standalone whitespace text nodes."""
    html = '<h2>Still doing it<!-- --> <span>all yourself?</span></h2>'
    assert _visible_text(_el(html, "h2")) == "Still doing it all yourself?"


def test_block_level_boundary_separates_words():
    """display:block spans are visual line breaks even with no whitespace."""
    html = (
        '<h1><span style="display:block">Watch what happens</span>'
        '<span style="display:block">when AI meets</span></h1>'
    )
    assert _visible_text(_el(html)) == "Watch what happens when AI meets"


def test_block_tag_boundary_separates_words():
    html = "<h1><div>Pilot.</div><div>AI architect.</div></h1>"
    assert _visible_text(_el(html)) == "Pilot. AI architect."


def test_inline_span_does_not_invent_spaces():
    """Per-character inline spans must not become 'W a t c h'."""
    html = "<h1><span>W</span><span>a</span><span>t</span><span>c</span><span>h</span></h1>"
    assert _visible_text(_el(html)) == "Watch"


def test_comments_are_not_text():
    html = "<h1>Real<!-- hidden comment --></h1>"
    assert _visible_text(_el(html)) == "Real"


def test_fully_decorative_element_falls_back_instead_of_empty():
    """Never report an empty heading; downstream reads that as 'missing'."""
    html = '<h1><span aria-hidden="true">Only decorative</span></h1>'
    assert _visible_text(_el(html)) == "Only decorative"


def test_whitespace_is_collapsed():
    html = "<h1>  Lots   of\n\n   space  </h1>"
    assert _visible_text(_el(html)) == "Lots of space"


def test_parse_html_headings_use_visible_text():
    """End to end through parse_html, mirroring the real page structure."""
    html = (
        "<html><head><title>T</title></head><body>"
        '<h1><span class="sr-only">Watch what happens</span>'
        '<span aria-hidden="true"><span>W</span><span>W</span></span></h1>'
        '<h2>Still doing it<!-- --> <span>all yourself?</span></h2>'
        "</body></html>"
    )
    result = parse_html(html, base_url="https://example.com")
    assert result["h1"] == ["Watch what happens"]
    assert result["h2"] == ["Still doing it all yourself?"]


def test_word_count_excludes_decorative_duplicates():
    real = "<html><body><p>one two three four five</p></body></html>"
    padded = (
        "<html><body><p>one two three four five</p>"
        '<p aria-hidden="true">six seven eight nine ten</p></body></html>'
    )
    assert parse_html(real)["word_count"] == parse_html(padded)["word_count"] == 5
