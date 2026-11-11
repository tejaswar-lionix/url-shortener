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


if __name__ == "__main__":
    unittest.main()
