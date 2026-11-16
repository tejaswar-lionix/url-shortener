#!/usr/bin/env python3
"""Encode URLs as short base62 codes with optional JSON persistence."""
import json
import os
import re

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALIAS_PATTERN = re.compile(r"^[A-Za-z0-9_-]{3,32}$")


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
        self._hits = {}
        if store_path and os.path.exists(store_path):
            self._restore()

    def shorten(self, url, alias=None):
        if not url.startswith(("http://", "https://")):
            raise ValueError("url must start with http:// or https://")
        if alias is not None:
            if not ALIAS_PATTERN.match(alias):
                raise ValueError("alias must be 3-32 letters, digits, _ or -")
            if alias in self._urls:
                raise ValueError("alias already in use")
            code = alias
        else:
            self._counter += 1
            code = encode_id(self._counter)
        self._urls[code] = url
        self._persist()
        return code

    def resolve(self, code):
        if code not in self._urls:
            return None
        self._hits[code] = self._hits.get(code, 0) + 1
        self._persist()
        return self._urls[code]

    def stats(self):
        return dict(self._hits)

    def list_links(self):
        return dict(self._urls)

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
            json.dump(
                {
                    "counter": self._counter,
                    "urls": self._urls,
                    "hits": self._hits,
                },
                handle,
                indent=2,
            )

    def _restore(self):
        with open(self.store_path, encoding="utf-8") as handle:
            data = json.load(handle)
        self._counter = data.get("counter", 0)
        self._urls = data.get("urls", {})
        self._hits = data.get("hits", {})
