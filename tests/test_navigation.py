import unittest

from src.navigation import (
    MAX_RESULTS, PHRASES_PREFIX, TEMPLATES_PREFIX, parse_query, select_results,
)


class _Item:
    def __init__(self, name):
        self.name = name


def _score(query, name):
    # Simple deterministic matcher to test selection independently of Ulauncher.
    if name.casefold().startswith(query.casefold()):
        return 100
    if query.casefold() in name.casefold():
        return 70
    return 0


class NavigationTests(unittest.TestCase):
    def test_empty_query_returns_compact_home(self):
        self.assertEqual(parse_query(""), ("home", ""))
        self.assertEqual(parse_query("   "), ("home", ""))
        self.assertEqual(parse_query(None), ("home", ""))

    def test_direct_search_is_cross_category(self):
        self.assertEqual(parse_query("知道"), ("all", "知道"))
        self.assertEqual(parse_query("Cora"), ("all", "Cora"))

    def test_browse_phrases_and_filter(self):
        self.assertEqual(parse_query(PHRASES_PREFIX), ("phrases", ""))
        self.assertEqual(parse_query(PHRASES_PREFIX + "知道"), ("phrases", "知道"))

    def test_browse_templates_and_filter(self):
        self.assertEqual(parse_query(TEMPLATES_PREFIX), ("templates", ""))
        self.assertEqual(parse_query(TEMPLATES_PREFIX + "Cora"), ("templates", "Cora"))

    def test_backspacing_prefix_restores_cross_search(self):
        self.assertEqual(parse_query("常用短语"), ("all", "常用短语"))
        self.assertEqual(parse_query(""), ("home", ""))

    def test_empty_category_shows_only_five(self):
        items = [_Item(str(i)) for i in range(15)]
        self.assertEqual([x.name for x in select_results(items, "", _score, 20)],
                         ["0", "1", "2", "3", "4"])

    def test_search_excludes_nonmatches_and_ranks(self):
        items = [_Item("再知道"), _Item("继续"), _Item("知道了")]
        self.assertEqual([x.name for x in select_results(items, "知道", _score)],
                         ["知道了", "再知道"])

    def test_search_preserves_order_on_score_ties(self):
        items = [_Item("知道了"), _Item("知道呀")]
        self.assertEqual([x.name for x in select_results(items, "知道", _score)],
                         ["知道了", "知道呀"])

    def test_bad_result_limit_is_safe(self):
        items = [_Item("知道了")]
        self.assertEqual(len(select_results(items, "", _score, "bad")), 1)
        self.assertEqual(len(select_results(items, "", _score, 0)), 1)


if __name__ == "__main__":
    unittest.main()
