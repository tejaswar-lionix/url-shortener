# url-shortener

Base62 URL shortener with JSON persistence.

## Usage

```bash
python3 -c "from shortener import *; s=Shortener(); print(s.shorten('https://example.com'))"
python3 -c "from shortener import *; s=Shortener(); print(s.shorten('https://example.com', alias='my-link'))"
python3 -c "from shortener import *; s=Shortener(); s.shorten('https://example.com'); s.resolve('1'); print(s.stats())"
python3 -c "from shortener import *; s=Shortener(); s.shorten('https://example.com'); print(s.list_links())"
```

## Features

- Base62 codes generated from a counter
- Custom aliases via Shortener.shorten(url, alias=None)
- URL validation and persistence
- Persisted hit counters with Shortener.stats()
- Delete short codes with Shortener.delete(code)
- Inspect all links with Shortener.list_links()

## Tests

```bash
python3 -m unittest -q
```

## License

MIT
