import unittest

from proseclean import clean


class CleanTests(unittest.TestCase):
    def test_removes_invisibles(self):
        out, rep = clean("Hola​ mundo﻿")
        self.assertEqual(out, "Hola mundo")
        self.assertEqual(rep.changes["invisible characters removed"], 2)

    def test_removes_tag_characters(self):
        out, _ = clean("a\U000e0041b")
        self.assertEqual(out, "ab")

    def test_exotic_spaces(self):
        out, _ = clean("a b c")
        self.assertEqual(out, "a b c")

    def test_typography_standard_only(self):
        s = "“hola”…"
        self.assertEqual(clean(s, "standard")[0], '"hola"...')
        self.assertEqual(clean(s, "light")[0], s)

    def test_repairs_mojibake_without_damaging_neighbours(self):
        s = "Canción â€™ fin — raya"
        out, _ = clean(s, "light")
        self.assertIn("Canción", out)
        self.assertIn("’", out)
        self.assertIn("—", out)

    def test_dashes_flagged_not_changed(self):
        out, rep = clean("uno — dos")
        self.assertIn("—", out)
        self.assertIn("long dashes (review by hand)", rep.flags)

    def test_chat_residue(self):
        out, _ = clean("texto【source】 <think>x</think>fin")
        self.assertEqual(out, "texto fin")

    def test_phrases_flagged_not_rewritten(self):
        out, rep = clean("Cabe destacar esto.")
        self.assertEqual(out, "Cabe destacar esto.")
        self.assertTrue(rep.flags)

    def test_clean_text_is_untouched(self):
        s = "Un texto normal, con tildes: canción."
        out, rep = clean(s)
        self.assertEqual(out, s)
        self.assertTrue(rep.clean)

    def test_bad_level(self):
        with self.assertRaises(ValueError):
            clean("x", "wild")


if __name__ == "__main__":
    unittest.main()
