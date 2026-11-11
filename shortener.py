#!/usr/bin/env python3
"""Encode URLs as short base62 codes with optional JSON persistence."""
import json
import os

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode_id(number):
    if number <= 0:
        raise ValueError("number must be positive")
    digits = []
    while number:
        number, remainder = divmod(number, len(ALPHABET))
        digits.append(ALPHABET[remainder])
    return "".join(reversed(digits))


class Shortener:
    def __init__(self, store_path=None):
        self.store_path = store_path
        self._counter = 0
        self._urls = {}
        if store_path and os.path.exists(store_path):
            self._restore()

    def shorten(self, url):
        if not url.startswith(("http://", "https://")):
            raise ValueError("url must start with http:// or https://")
        self._counter += 1
        code = encode_id(self._counter)
        self._urls[code] = url
        self._persist()
        return code

    def resolve(self, code):
        return self._urls.get(code)

    def delete(self, code):
        """Remove a short code. Returns True when it existed."""
        if code in self._urls:
            del self._urls[code]
            self._persist()
            return True
        return False

    def _persist(self):
        if not self.store_path:
            return
        with open(self.store_path, "w", encoding="utf-8") as handle:
            json.dump({"counter": self._counter, "urls": self._urls}, handle, indent=2)

    def _restore(self):
        with open(self.store_path, encoding="utf-8") as handle:
            data = json.load(handle)
        self._counter = data.get("counter", 0)
        self._urls = data.get("urls", {})
