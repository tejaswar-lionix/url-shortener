import os
import tempfile
import unittest

from shortener import Shortener, encode_id


class ShortenerTests(unittest.TestCase):
    def test_encode_id_uses_base62(self):
        self.assertEqual(encode_id(1), "1")
        self.assertEqual(encode_id(61), "Z")
        self.assertEqual(encode_id(62), "10")

    def test_encode_rejects_non_positive(self):
        with self.assertRaises(ValueError):
            encode_id(0)

    def test_shorten_and_resolve(self):
        shortener = Shortener()
        code = shortener.shorten("https://example.com/very/long/path")
        self.assertEqual(shortener.resolve(code), "https://example.com/very/long/path")

    def test_shorten_rejects_bad_url(self):
        with self.assertRaises(ValueError):
            Shortener().shorten("example.com")

    def test_unknown_code_returns_none(self):
        self.assertIsNone(Shortener().resolve("missing"))

    def test_persistence_roundtrip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "links.json")
            code = Shortener(path).shorten("https://example.com")
            self.assertEqual(Shortener(path).resolve(code), "https://example.com")


class HitStatsTests(unittest.TestCase):
    def test_resolve_increments_hits(self):
        shortener = Shortener()
        code = shortener.shorten("https://example.com")
        shortener.resolve(code)
        self.assertEqual(shortener.stats()[code], 1)

    def test_repeated_resolves_accumulate(self):
        shortener = Shortener()
        code = shortener.shorten("https://example.com")
        for _ in range(3):
            shortener.resolve(code)
        self.assertEqual(shortener.stats()[code], 3)

    def test_unknown_code_does_not_create_hit(self):
        shortener = Shortener()
        self.assertIsNone(shortener.resolve("missing"))
        self.assertEqual(shortener.stats(), {})

    def test_hits_survive_persistence_roundtrip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "links.json")
            shortener = Shortener(path)
            code = shortener.shorten("https://example.com")
            shortener.resolve(code)
            shortener.resolve(code)
            self.assertEqual(Shortener(path).stats()[code], 2)

    def test_stats_returns_a_copy(self):
        shortener = Shortener()
        code = shortener.shorten("https://example.com")
        shortener.resolve(code)
        stats = shortener.stats()
        stats[code] = 99
        self.assertEqual(shortener.stats()[code], 1)


class DeleteTests(unittest.TestCase):
    def test_delete_removes_existing_code(self):
        from shortener import Shortener

        shortener = Shortener()
        code = shortener.shorten("https://example.com")
        self.assertTrue(shortener.delete(code))
        self.assertIsNone(shortener.resolve(code))

    def test_delete_returns_false_for_unknown_code(self):
        from shortener import Shortener

        self.assertFalse(Shortener().delete("missing"))


if __name__ == "__main__":
    unittest.main()
