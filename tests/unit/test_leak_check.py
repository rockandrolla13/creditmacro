"""Copyright leak guard: no long verbatim run from raw normalized-md may appear in a wiki page."""
from __future__ import annotations

from tools.leak_check import assert_clean, longest_verbatim_run

RAW = ("The maximum entropy principle selects the distribution that is least committal "
       "with respect to missing information while honoring the stated moment constraints "
       "exactly and reproducing the observed market price of the underlying axis.")


def test_paraphrase_has_short_verbatim_run():
    paraphrase = "Max-entropy picks the least-committal distribution that still matches the price."
    assert longest_verbatim_run(paraphrase, RAW) < 25


def test_copied_passage_is_a_long_run():
    leaked = "Intro. " + RAW + " End."
    assert longest_verbatim_run(leaked, RAW) >= 25


def test_assert_clean_flags_a_leaking_card(tmp_path):
    raw_dir = tmp_path / "raw"; raw_dir.mkdir()
    wiki_dir = tmp_path / "wiki"; wiki_dir.mkdir()
    (raw_dir / "src1.md").write_text(RAW)
    # paraphrase card → clean
    (wiki_dir / "ok.md").write_text("Method card: the engine tilts a prior to match the price.")
    assert assert_clean(wiki_dir, raw_dir, max_run_words=25) == []
    # leaking card → flagged
    (wiki_dir / "bad.md").write_text("# Card\n\n" + RAW)
    violations = assert_clean(wiki_dir, raw_dir, max_run_words=25)
    assert any("bad" in v for v in violations)
