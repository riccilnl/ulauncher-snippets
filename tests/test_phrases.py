import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from src.phrases import get_phrases


class PhraseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "phrases.json"

    def write(self, value):
        self.path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    def test_multiple_chinese_phrases_from_one_file(self):
        self.write({"知道了": "知道了", "好了": "好了", "复核": "请复核\n全部依据。"})
        phrases = get_phrases(self.temp.name)
        self.assertEqual([p.name for p in phrases], ["知道了", "好了", "复核"])
        self.assertEqual(phrases[2].render(copy_mode="wl"), ("text/plain", "请复核\n全部依据。"))
        self.assertEqual(phrases[2].description, "请复核 全部依据。")
        self.assertIsNone(phrases[0].next_variable())
        self.assertIsNone(phrases[0].file_path_template)

    def test_missing_file_is_optional(self):
        self.assertEqual(get_phrases(self.temp.name), [])

    def test_invalid_json_does_not_crash(self):
        self.path.write_text("{bad", encoding="utf-8")
        self.assertEqual(get_phrases(self.temp.name), [])

    def test_non_object_and_invalid_entries(self):
        self.write(["x"])
        self.assertEqual(get_phrases(self.temp.name), [])
        self.write({"keep": "ok", "bad": 123, " ": "blank title"})
        self.assertEqual([(p.name, p.content) for p in get_phrases(self.temp.name)], [("keep", "ok")])

    def test_automatic_reload_when_file_changes(self):
        self.write({"foo": "one"})
        self.assertEqual(get_phrases(self.temp.name)[0].content, "one")
        self.write({"foo": "replacement"})
        self.assertEqual(get_phrases(self.temp.name)[0].content, "replacement")

    def test_jinja_placeholders_in_plain_phrases_remain_literal(self):
        self.write({"literal": '{{ vars("project") }}'})
        self.assertEqual(get_phrases(self.temp.name)[0].render()[1], '{{ vars("project") }}')


if __name__ == "__main__":
    unittest.main()
